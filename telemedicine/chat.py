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
from telemedicine.retrievers import RetrieveFromDocuments


class Chat:
    """
    Class to manage chat interactions and retrieve information from documents.
    """
    
    def __init__(self):
        self.history = []
        

    def add_history(self, 
                    message_type: str, 
                    message: str) -> None:
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
        timestamp = datetime.now()
        message = Message(
            message_id=message_id,
            conversation_index=conversation_index,
            timestamp=timestamp,
            message_type=message_type,
            message_str=message
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
        n_messages = min(num_messages, len(assistant_messages))
        for message in assistant_messages[-n_messages:]:
            index = message.conversation_index
            user_message, assistant_message = self.get_message_pair_by_index(index)
            message_pair_str += user_message.get_message_dialogue() + '\n'
            message_pair_str += assistant_message.get_message_dialogue() + '\n'
        return message_pair_str


    def get_response(self, question: str) -> str:
        """
        Process the given question and retrieve the appropriate response.
        This method wraps several interaction with the retrievers agent.

        Args:
            question (str): The question to process and retrieve the response for.

        Returns:
            str: The response generated by the retrieval process.
        """
        self.add_history('user', question)
        response = self.get_final_document_answers(question)
        self.add_history('assistant', response)
        return response
    
    
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