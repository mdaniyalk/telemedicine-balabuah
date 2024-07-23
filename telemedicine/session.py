"""
Module for ChatSession Class.
"""

import pickle
import os
from typing import Any, Dict
import markdown2 as markdown
from telemedicine.core.base import ConfigurationMixin
from telemedicine.core.configuration import Configuration

from telemedicine.core.tools import generate_id, get_date
from telemedicine.core.thread import multithreading
from telemedicine.core.directory_utilities import find_file, make_dir
from telemedicine.chat import Chat


class ChatSession(ConfigurationMixin):
    """
    Class representing a chat session.
    """
    def __init__(self, config: Configuration = None):
        super().__init__(config=config)
        self.session_id:str = None
        self.chat_session:Chat = None
        self.filename:str = None


    def load(self, session_id: str) -> None:
        """
        Load a chat session.

        Args:
            session_id (str): The session ID.

        Returns:
            None
        """
        self.session_id = session_id
        base_path = os.path.join(os.getcwd(), 'user-session-data')
        filename = find_file(f"{self.session_id}.session", base_path)
        self.filename = filename
        self.load_from_file(filename)
    

    def load_from_file(self, filename: str) -> None:
        """
        Load a chat session from a file.

        Args:
            filename (str): The name of the file to load the session from.

        Returns:
            None
        """

        if self.session_id is None:
            self.session_id = os.path.basename(filename).replace(".session", "")
        with open(filename, "rb") as file:
            serialize = pickle.load(file)
            chat_session = Chat(self.config)
            chat_session.history = serialize["history"]
            chat_session.is_question_complete = serialize["is_question_complete"]
            chat_session.path_vectorstores = serialize["path_vectorstores"]
            chat_session.is_document_found = serialize["is_document_found"]
            chat_session.complete_response = serialize["complete_response"]
            chat_session.initial_question = serialize["initial_question"]
            chat_session.additional_details = serialize["additional_details"]
            chat_session.document_candidates = serialize["document_candidates"]
            chat_session.root_document_path = serialize["root_document_path"]
            self.chat_session = chat_session


    def delete_session(self):
        """
        Delete the current chat session file.

        Returns:
            None
        """

        os.remove(self.filename)


    def initialize(self):
        """
        Initialize a new chat session.

        Returns:
            None
        """

        self.session_id = self._initialize_session()
    

    def save_session(self):
        """
        Save the chat session.

        Returns:
            None
        """

        filename = self.filename
        chat_session = self.copy_chat()
        save_session(chat_session, filename)
    

    def copy_chat(self) -> Chat:
        """
        Copy the chat session.

        Returns:
            Chat: The copied chat session.
        """

        serialize = {}
        serialize["history"] = self.chat_session.history
        serialize["is_question_complete"] = self.chat_session.is_question_complete
        serialize["path_vectorstores"] = self.chat_session.path_vectorstores
        serialize["is_document_found"] = self.chat_session.is_document_found
        serialize["complete_response"] = self.chat_session.complete_response
        serialize["initial_question"] = self.chat_session.initial_question
        serialize["additional_details"] = self.chat_session.additional_details
        serialize["document_candidates"] = self.chat_session.document_candidates
        serialize["root_document_path"] = self.chat_session.root_document_path
        return serialize


    def _initialize_session(self) -> str:
        """
        Initialize a new session.

        Returns:
            str: The session ID.
        """

        session_id = generate_id()
        chat_session = Chat(self.config)
        self.chat_session = chat_session
        dirname = os.path.join(os.getcwd(), 'user-session-data')
        make_dir(dirname)
        today = get_date()
        dirname = os.path.join(dirname, today)
        make_dir(dirname)
        filepath = os.path.join(dirname, f"{session_id}.session")
        self.filename = filepath
        self.save_session()
        return session_id
    

    def get_response(self, msg: str, html=True) -> str:
        """
        Get the response to a given message.

        Args:
            msg (str): The message to get a response for.
            html (bool, optional): Whether to format the response as HTML. Defaults to False.

        Returns:
            str: The response to the message.
        """

        response = self.chat_session.get_response(msg)
        if html:
            response = markdown.markdown(response, extras=["tables", "cuddled-lists", "wiki-tables"])
        return response
    

    def get_dict(self, with_conversation: bool = False) -> Dict[str, Any]:
        """
        Get a dictionary representation of the chat session.

        Args:
            with_conversation (bool, optional): Whether to include the conversation history. Defaults to False.

        Returns:
            Dict[str, Any]: A dictionary containing the session data.
        """

        try:
            timestamp = self.chat_session.history[0].timestamp,
            session_title = self.chat_session.history[0].message_str
            conversation = self.chat_session.get_conversation()
            response = {
                "session_id": self.session_id,
                "timestamp": timestamp,
                "session_title": session_title
            }
            if with_conversation:
                response["conversation"] = conversation
            return response
        except Exception as e:
            return None

    @classmethod
    def get_session_data(cls, 
                         session_filename: str = None, 
                         session_id: str = None,
                         with_conversation: bool = False) -> Dict[str, Any]:
        """
        Get session data given a filename or session ID.

        Args:
            session_filename (str, optional): The filename of the session data file. Defaults to None.
            session_id (str, optional): The session ID. Defaults to None.
            with_conversation (bool, optional): Whether to include the conversation history. Defaults to False.

        Returns:
            Dict[str, Any]: A dictionary containing the session data.

        Raises:
            ValueError: If neither session_filename nor session_id is provided.
        """
       
        if session_filename is None and session_id is None:
            raise ValueError("Please provide a session filename or session id.")
        chat_session = cls()
        if session_filename:
            chat_session.load_from_file(session_filename)
        elif session_id:
            chat_session.load(session_id)
        return chat_session.get_dict(with_conversation)

    

def save_session(session, filename):
    """
    Save the chat session to a file.

    Args:
        session (ChatSession): The chat session.
        filename (str): The filename to save the chat session to.

    Returns:
        None
    """

    with open(filename, "wb") as file:
        pickle.dump(session, file)


def get_all_session(offset, per_page, order):
    """
    Get all the chat sessions.

    Args:
        offset (int): The offset.
        per_page (int): The number of items per page.
        order (str): The order of the items.

    Returns:
        list: A list of chat sessions.
    """

    base_path = os.path.join(os.getcwd(), 'user-session-data')
    all_session = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".session"):
                all_session.append(os.path.join(root, file))
    start = offset
    end = offset + per_page
    all_session_data = multithreading(ChatSession.get_session_data, all_session)
    all_session_data = [session for session in all_session_data if session is not None]
    if order == 'latest':
        all_session = sorted(all_session_data, key=session_sorting_rules, reverse=True)
    else:
        all_session = sorted(all_session_data, key=session_sorting_rules)
    return all_session[start:end]


def session_sorting_rules(obj):
    """
    Sorting rules for the session.

    Args:
        obj (str): The object to sort.

    Returns:
        str: The sorted object.
    """

    datetime = obj["timestamp"]
    return datetime
