from typing import Any, Dict, List, Optional, Tuple
import os
from datetime import datetime

from telemedicine.core.base import (
    ConfigurationMixin,
    openai_embedding,
    Message,
    calculate_similarity
)
from telemedicine.core.configuration import Configuration
from telemedicine.core.translate import translate
from telemedicine.core.prompt_template import change_document_template, greeting_prompt_template
from telemedicine.retrievers import (
    RetrieveDetailQuestion,
    RetrieveDocuments,
    RetrieveFinalDocuments,
    RetrieveFromDocuments,
    RetrievefromMultiDocuments, 
)


class Chat(ConfigurationMixin):
    """
    Class to manage chat interactions and retrieve information from documents.
    """
    
    def __init__(self, config: Optional[Configuration] = None):
        super().__init__(config=config)
        self.is_question_complete = False
        self.path_vectorstores = None
        self.is_document_found = False
        self.complete_response = None
        self.history = []
        self.initial_question = []
        self.additional_details = []
        self.document_candidates = []
        self.root_document_path = None
        

    def add_history(self, 
                    message_type: str, 
                    message: str, 
                    message_embedding: List[float]=None) -> None:
        """
        Add a message to the chat history.

        Args:
            message_type (str): The type of the message (e.g., 'user', 'assistant').
            message (str): The content of the message.
            message_embedding (List[float], optional): The embedding of the message. Defaults to None.

        Returns:
            None
        """

        conversation_index = self.get_last_conversation_index()
        message_id = f'{message_type}_{conversation_index}'
        if message_embedding is None:
            message_embedding = openai_embedding(text=message, config=self.config)
        timestamp = datetime.now()
        message = Message(
            message_id=message_id,
            conversation_index=conversation_index,
            timestamp=timestamp,
            message_type=message_type,
            message_str=message,
            message_embedding=message_embedding,
        )
        self.history.append(message)


    def get_last_conversation_index(self) -> int:
        """
        Get the index of the last conversation in the chat history.

        Returns:
            int: The index of the last conversation.
        """

        index = 0
        if len(self.history) > 0:
            for message in self.history:
                if message.conversation_index > index:
                    index = message.conversation_index
                    message_type = message.message_type
                    if message_type == 'assistant':
                        index += 1
        return index
    

    def get_message_pair_by_index(self, index: int) -> Tuple[str, str]:
        """
        Get a pair of messages (user and assistant) by conversation index.

        Args:
            index (int): The conversation index.

        Returns:
            Tuple[str, str]: A tuple containing the user message and the assistant message.
        """

        assistant_message = None
        user_message = None
        for message in self.history:
            if message.conversation_index == index:
                if message.message_type == 'assistant':
                    assistant_message = message
                elif message.message_type == 'user':
                    user_message = message
        return user_message, assistant_message
    

    def get_n_last_message_pair(self, num_messages: int) -> str:
        """
        Get the last n pairs of messages (user and assistant) from the chat history.

        Args:
            num_messages (int): The number of message pairs to retrieve.

        Returns:
            str: A string representation of the last n message pairs.
        """

        assistant_messages = [message for message in self.history if message.message_type == 'assistant']
        message_pair_str = ''
        for message in assistant_messages[-num_messages:]:
            index = message.conversation_index
            user_message, assistant_message = self.get_message_pair_by_index(index)
            message_pair_str += user_message.get_message_dialogue() + '\n'
            message_pair_str += assistant_message.get_message_dialogue() + '\n'
        return message_pair_str
    

    def get_conversation(self) -> List[Dict[str, str]]:
        """
        Retrieve the entire conversation history.

        Returns:
            List[Dict[str, str]]: A list of dictionaries, each containing the message type, message content, and timestamp.
        """

        conversations = []
        for message in self.history:
            conversation = {}
            conversation['message_type'] = message.message_type
            conversation['message'] = message.message_str
            conversation['timestamp'] = message.timestamp
            conversations.append(conversation)
        return conversations


    def get_relevant_history(self, question_embedding: List[float]) -> str:
        """
        Retrieve the most relevant history based on the question embedding.

        Args:
            question_embedding (List[float]): The embedding of the current question.

        Returns:
            str: The most relevant message pair (user and assistant) from the history.
        """

        similarity_scores = []
        for message in self.history:
            similarity = calculate_similarity(message.message_embedding, question_embedding)
            similarity_scores.append(similarity)
        max_similarity = max(similarity_scores)
        max_similarity_index = similarity_scores.index(max_similarity)
        user_message, assistant_message = self.get_message_pair_by_index(max_similarity_index)
        message_pair = ''
        if user_message is not None:
            message_pair += user_message.get_message_dialogue()
        if assistant_message is not None:
            message_pair += assistant_message.get_message_dialogue() + '\n'
        return message_pair
    
    
    def prepare_history(self, question_embedding: List[float] = None) -> str:
        """
        Prepare the history to be included in the current context.

        Args:
            question_embedding (List[float], optional): The embedding of the current question. Defaults to None.

        Returns:
            str: A string representation of the relevant history to include.
        """

        if not self.is_question_complete:
            history = None
            if int(len(self.history)/2) > 0:
                if int(len(self.history)/2) == 1:
                    user_history = self.history[0].message_str
                    assistant_history = self.history[1].message_str
                    history = f"User: {user_history}\nAssistant: {assistant_history}"
                else:
                    user_history = self.history[len(self.history)-3].message_str
                    assistant_history = self.history[len(self.history)-2].message_str
                    history = f"User: {user_history}\nAssistant: {assistant_history}"
        else:
            history = ''
            if int(len(self.history)/2) > 1:
                history += self.get_n_last_message_pair(2)
                if int(len(self.history)/2) > 4 and question_embedding is not None:
                    relevant_history = self.get_relevant_history(question_embedding)
                    history = relevant_history + history
            else:
                history += self.get_n_last_message_pair(1)
        return history


    def get_response(self, question: str) -> str:
        """
        Process the given question and retrieve the appropriate response.
        This method wraps several interaction with the retrievers agent.

        Args:
            question (str): The question to process and retrieve the response for.

        Returns:
            str: The response generated by the retrieval process.
        """

        question_embedding = openai_embedding(question, config=self.config)
        self.add_history('user', question, question_embedding)
        if question == '\ganti-dokumen':
            response = self.get_ganti_dokumen_response()
            self.add_history('assistant', response)
            return response
        if not self.is_question_complete:
            initial_question = self.prepare_initial_question(question)
            status, response = self.get_initial_response(initial_question)
            print('response: ', response)
            if status == "not completed":
                self.add_history('assistant', response)
                return response
            elif status == "completed":
                if len(self.document_candidates) == 0:
                    self.is_question_complete = True
                    # get selection of document
                    question = response['refined_question']
                    folder_path = response['folder_path']
                    response = self.get_multi_document_answers(question, folder_path)
                    self.add_history('assistant', response)
                    return response
        else:
            response = self.get_multi_document_answers(question)
            self.add_history('assistant', response)
            return response
        

    def prepare_initial_question(self, question: str) -> str:
        """
        Prepare the initial question by appending any additional details provided by the user.

        Args:
            question (str): The initial question or additional details provided by the user.

        Returns:
            str: The prepared initial question.
        """

        if len(self.initial_question) ==0:
            # save the initial question
            self.initial_question.append(question)
        else:
            # save additional details if the initial question already filled
            self.additional_details.append(question)
        print('self.initial_question: ', self.initial_question)
        print('self.additional_details: ', self.additional_details)
        initial_question = self.initial_question[0] + ' ' + ' '.join(self.additional_details)
        print('initial_question: ', initial_question)
        return initial_question


    def get_initial_response(self, question: str) -> Tuple[str, str]:
        """
        Retrieval agent to retrieve the initial response for the given question.

        Args:
            question (str): The question to retrieve the initial response for.

        Returns:
            Tuple[str, str]: The status of the response and the response text.
        """

        history = self.prepare_history()
        print('question: ', question)
        response = RetrieveDetailQuestion.retrieve(
            question=question, history=history, config=self.config
        )
        if response["status"] == "not completed":
            response_text = response["question to user"]
            response_text = translate(response_text, "auto", "id")
            return response["status"], response_text
        else:
            return response["status"], response

    def get_multi_document_answers(self, question: str, folder_path: List = None) -> str:
        """
        Retrieval agent to retrieve the final answers from the documents for the given question.

        Args:
            question (str): The refined question.
            question_embedding (List[float]): The embedding of the question.

        Returns:
            str: The final answers from the documents.
        """
        if folder_path is not None:
            self.root_document_path = folder_path.split('/')

        history = self.prepare_history()
        response_text = RetrievefromMultiDocuments.retrieve(
            question=question, 
            history=history, 
            folder_path = self.root_document_path,
            config=self.config
        )
        response_text = translate(response_text, "auto", "id")
        response_text += "\n\n---\n\n"
        response_text += change_document_template()
        return response_text

    def get_document_selection(self, question: Dict[str, Any]) -> str:
        """
        Retrieval agent to retrieve a list of document candidates for the given question.

        Args:
            question (Dict[str, Any]): The question details including the folder path.

        Returns:
            str: The response text for document selection.
        """

        print(question)
        folder_path = question['folder_path'].split('/')
        config = Configuration.load('config.toml')
        folder_names = config('folder_names')
        folder_path = os.path.join(*folder_path[:len(folder_names)])
        self.root_document_path = folder_path
        response = RetrieveDocuments.retrieve(
            question=question, config=self.config
        )
        text_response = response['question']
        text_response = translate(text_response, "auto", "id")
        file_list = response['file_list']
        self.document_candidates = file_list
        status = response['status']
        return status, text_response


    def get_document_confirmation(self, question: str) -> Tuple[bool, str]:
        """
        Retrieval agent to confirm the document selection for the given question.

        Args:
            question (str): The question for document confirmation.

        Returns:
            Tuple[bool, str]: The status of the document confirmation and the response text.
        """

        status, response = RetrieveFinalDocuments.retrieve(
            question=question,
            document_candidates=self.document_candidates,
            root_document_path=self.root_document_path,
            config=self.config
        )
        if status:
            self.path_vectorstores = response[1]
            print("sudah apply path dan vectorstore")
            return status, question
        else:
            text_response = response['question']
            text_response = translate(text_response, "auto", "id")
            file_list = response['file_list']
            self.document_candidates = file_list
            return status, text_response


    def get_final_document_answers(self, question: str, question_embedding: List[float]) -> str:
        """
        Retrieval agent to retrieve the final answers from the documents for the given question.

        Args:
            question (str): The refined question.
            question_embedding (List[float]): The embedding of the question.

        Returns:
            str: The final answers from the documents.
        """

        history = self.prepare_history(question_embedding)
        response_text = RetrieveFromDocuments.retrieve(
            question=question, 
            history=history, 
            db_folder_paths=self.path_vectorstores,
            config=self.config
        )
        response_text = translate(response_text, "auto", "id")
        response_text += "\n\n---\n\n"
        response_text += change_document_template()
        return response_text
        

    def get_ganti_dokumen_response(self: str) -> str:
        """
        Reset the document selection and prompt the user for a new question.

        Returns:
            str: The response prompting the user for a new question.
        """
        self.is_question_complete = False
        self.path_vectorstores = None
        self.is_document_found = False
        self.complete_response = None
        self.initial_question = []
        self.additional_details = []
        self.document_candidates = []
        self.root_document_path = None
        response = greeting_prompt_template()
        return response
    