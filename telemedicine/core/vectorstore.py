"Vector store module for managing vector databases."
import os
import pickle
from typing import Any, Dict, List, Tuple
import certifi
from pymongo import MongoClient
from tqdm import tqdm

from langchain.vectorstores import MongoDBAtlasVectorSearch


from telemedicine.core.base import openai_chat, openai_embedding
from telemedicine.core.configuration import Configuration
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from telemedicine.core.file_loader import file_loader
from telemedicine.core.text_splitter import RecursiveTokenTextSplitter


class VectorDB:
    """
    Class for managing vector databases.
    """
    def __init__(self, 
                 model_name: str = None,
                 embedding_model: str = None, 
                 openai_api_key: str = None) -> None:
        """
        Initialize the VectorDB.

        Args:
            embedding_model (str): The embedding model to use.
            openai_api_key (str): The OpenAI API key.
        """
        self.vectorstore = None
        if embedding_model is None:
            raise ValueError("Please set the embedding_model in param")
        
        if openai_api_key is None:
            raise ValueError("Please set the openai_api_key in param")
        
        if model_name is None:
            raise ValueError("Please set the model_name in param")

        self.model = model_name
        self.embedding: OpenAIEmbeddings = OpenAIEmbeddings(
            openai_api_key=openai_api_key, model=embedding_model)
        self.openai_api_key: str = openai_api_key
        self.embedding_model: str = embedding_model
        self.mongo_uri = os.getenv('MONGO_URI')
        self.client = MongoClient(self.mongo_uri, tlsCAFile=certifi.where())
        self.db_name = os.getenv('MONGO_DB_VECTOR')
        self.collection_name = os.getenv('MONGO_COLLECTION_VECTOR')
        self.collection = self.client[self.db_name][self.collection_name]
        self.index_name = os.getenv('MONGO_INDEX_NAME')


    def load_documents_from_files(self, filepath: list[str])-> None:
        """
        Load documents from files.

        Args:
            filepath (list[str]): The path to the documents.
        """
        splitted_document = []
        for file in filepath:
            extracted_document = file_loader(file)
            text_splitter = RecursiveTokenTextSplitter(chunk_size = 400,
                                                       chunk_overlap = 50)
            splitted_document.extend(text_splitter.split_documents(extracted_document))

        self.vectorstore = MongoDBAtlasVectorSearch.from_documents(
            documents=splitted_document,
            embedding=self.embedding,
            collection=self.collection, 
            index_name=self.index_name
        )
                 
        
    def as_retriever(self, 
                     search_type: str, 
                     search_kwargs: dict):
        """
        Convert the vector database to a retriever.

        Args:
            search_type (str): The type of search to perform.
            search_kwargs (dict): The keyword arguments for the search.

        Returns:
            Retriever: The retriever.
        """
        return self.vectorstore.as_retriever(search_type=search_type, search_kwargs=search_kwargs)
    
    def load_local(self) -> None:
        """
        Load the vector database from a local folder.

        Args:
            folder_path (str): The path to the folder containing the vector database.
        """
        
        self.vectorstore = MongoDBAtlasVectorSearch(
            embedding=self.embedding,
            collection=self.collection, 
            index_name=self.index_name
        )
        
    
    def similarity_search_with_score_by_vector(
            self, 
            vector: List[float], 
            top_k: int = 5,
            **kwargs: Any
        ) -> List[Tuple[Document, float]]:
        """
        Search for similar documents by vector.

        Args:
            vector (list): The vector to search for.
            top_k (int): The number of similar documents to return.

        Returns:
            list: The list of similar documents.
        """
        return self.vectorstore.similarity_search_with_score_by_vector(
            embedding=vector, k=top_k, **kwargs
        )
    
    def max_marginal_relevance_search_with_score_by_vector(
            self, 
            vector: List[float], 
            top_k: int = 5,
            **kwargs: Any
        ) -> List[Tuple[Document, float]]:
        """
        Search for similar documents using max marginal relevance.

        Args:
            vector (list): The vector to search for.
            top_k (int): The number of similar documents to return.

        Returns:
            list: The list of similar documents.
        """
        return self.vectorstore.max_marginal_relevance_search_with_score_by_vector(
            embedding=vector, k=top_k, **kwargs
        )
    