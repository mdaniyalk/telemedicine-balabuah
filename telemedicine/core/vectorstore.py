"Vector store module for managing vector databases."
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import pickle
from typing import Any, Dict, List, Tuple
import certifi
from pymongo import MongoClient
import requests
from tqdm import tqdm
from fake_useragent import UserAgent

from langchain_community.vectorstores.mongodb_atlas import MongoDBAtlasVectorSearch
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings



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
                 embedding_model: str = None) -> None:
        """
        Initialize the VectorDB.

        Args:
            embedding_model (str): The embedding model to use.
            openai_api_key (str): The OpenAI API key.
        """
        self.vectorstore = None
        if embedding_model is None:
            raise ValueError("Please set the embedding_model in param")
        
        if model_name is None:
            raise ValueError("Please set the model_name in param")
        load_dotenv('.env')
        openai_api_key = os.getenv('OPENAI_API_KEY')
        self.model = model_name
        # self.embedding: OpenAIEmbeddings = OpenAIEmbeddings(
        #     openai_api_key=openai_api_key, model=embedding_model)
        self.openai_api_key: str = openai_api_key
        # self.embedding_model: str = embedding_model
        self.embedding: FastEmbedEmbeddings = FastEmbedEmbeddings(
            model_name="BAAI/bge-small-en-v1.5")
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
        for file in tqdm(filepath, desc="Loading documents"):
            try:
                extracted_document = file_loader(file)
                text_splitter = RecursiveTokenTextSplitter(chunk_size = 256,
                                                        chunk_overlap = 50)
                splitted_document.extend(text_splitter.split_documents(extracted_document))
            except Exception as e:
                print(f"Error loading document: {e}")
                continue

        self.vectorstore = MongoDBAtlasVectorSearch.from_documents(
            documents=splitted_document,
            embedding=self.embedding,
            collection=self.collection, 
            index_name=self.index_name
        )

    def load_document_from_folder(self, folder_path: str) -> None:
        """
        Load documents from a folder.

        Args:
            folder_path (str): The path to the folder containing the documents.
        """
        file_list = os.listdir(folder_path)
        self.load_documents_from_files([os.path.join(folder_path, file) for file in file_list])
        
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
    

def weburl_to_txt(url: str, savepath: str) -> None:
    """
    Convert a web URL to text and save it to a file.

    Args:
        url (str): The URL to convert.
        savepath (str): The path where the text file will be saved.
    """
    session = requests.Session()
    user_agent = UserAgent()

    random_user_agent = user_agent.random

    headers = {'user-agent': random_user_agent}
    html_doc = session.get(url, headers=headers)
    session.close()
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    _txt = soup.get_text()
    _txt = ' '.join(_txt.split())
    
    with open(savepath, 'w', encoding='utf-8') as f:
        f.write(_txt)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Load documents from files into the vector store.")
    parser.add_argument("--folder_path", type=str, help="The path to the folder containing the documents.")
    args = parser.parse_args()

    vectorstore = VectorDB(
        model_name="",
        embedding_model="BAAI/bge-small-en-v1.5" 
    )
    vectorstore.load_documents_from_files(args.folder_path)
