"""
Module for ChatSession Class.
"""

from dataclasses import dataclass
import os
import random
import string
import certifi
from pymongo import MongoClient
from typing import Any, Dict
import markdown2 as markdown

from telemedicine.chat import Chat

@dataclass
class SessionObject:
    session_id: str
    session_data: list


class ChatSession:
    """
    Class representing a chat session.
    """
    def __init__(self):
        self.session_id : str = None
        self.chat_session : Chat = None
        self.session_object : SessionObject = None
        self.mongo_uri = os.getenv('MONGO_URI')
        self.client = MongoClient(self.mongo_uri, tlsCAFile=certifi.where())
        self.db_name = os.getenv('MONGO_DB_SESSION')
        self.collection_name = os.getenv('MONGO_COLLECTION_SESSION')
        self.collection = self.client[self.db_name][self.collection_name]


    def load(self, session_id: str) -> None:
        """
        Load a chat session.

        Args:
            session_id (str): The session ID.

        Returns:
            None
        """
        self.session_id = session_id
        existing_entry = self.collection.find_one({'session_id': self.session_id})
        if existing_entry is not None:
            self.session_object = SessionObject(
                session_id=existing_entry['session_id'],
                session_data=existing_entry['session_data']
            )
            self.chat_session = self.deserialize_chat()


    def post_object(self):
        try:
            existing_entry = self.collection.find_one({'session_id': self.session_object.session_id})
        except Exception as e:
            print(f"Error finding session: {e}")
            existing_entry = None
            
        try:
            if existing_entry is not None:
                self.collection.update_one(
                    {'session_id': self.session_object.session_id}, 
                    {'$set': {'session_data': self.session_object.session_data}}
                )
            else:
                self.collection.insert_one(
                    {
                        'session_id': self.session_object.session_id, 
                        'session_data': self.session_object.session_data
                    }
                )
        except Exception as e:
            raise Exception(f"Error updating or inserting session: {e}") from e


    def initialize(self):
        """
        Initialize a new chat session.

        Returns:
            None
        """
        alphanumeric = string.ascii_letters + string.digits
        self.session_id = ''.join(random.choices(alphanumeric, k=16))
        self.chat_session = Chat()
        self.session_object = SessionObject(session_id=self.session_id, session_data=[])


    def serialize_chat(self):
        pass 
        #TODO: Return session_data as a list of serialized messages

    def deserialize_chat(self):
        pass
        #TODO: Return chat object with loaded history
    

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
    
