import os
from typing import Any, Dict, List, Tuple
import json

from telemedicine.core.base import (
    calculate_similarity, 
    openai_chat, 
    openai_embedding, 
    BaseRetrievers,
    
)
from telemedicine.core.ensemble_retrivers import CustomEnsembleRetriever
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.globals import set_debug 
from langchain_community.chat_models.openai import ChatOpenAI
from telemedicine.core.vectorstore import VectorDB
from telemedicine.core.prompt_template import (
    multi_query_retriver_prompt,
    retrieval_qa_prompt
)
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from telemedicine.core.retrieval_qa import CustomRetrievalQA


set_debug(True)

class Retrieval(BaseRetrievers):
    """
    Class to retrieve information from documents using a retrieval QA system.
    """

    def __init__(self, **kwargs) -> None:
        self.prompt = retrieval_qa_prompt()
        self.llm = ChatOpenAI(
            model_name="llama-3.2-1b-preview",
            max_tokens=4096,  
            openai_api_key=os.getenv('GROQ_API_KEY'), 
            openai_api_base="https://api.groq.com/openai/v1",
            temperature=0.1
        )
        self.token_usage = []

    def result(self, 
               question: str,
               history: str = None,
               return_usage: bool = True,
               **kwargs: Any) -> str:
        """
        Retrieve the result for a given question.

        Args:
            question (str): The question to retrieve the result for.
            history (str): The history of interactions.

        Returns:
            The result of the retrieval process as a string.
        """
        self.prepare_retrivers(**kwargs)
        # self.ensemble_retriever = None
        qa = CustomRetrievalQA(llm=self.llm, 
                               retriever=self.ensemble_retriever, 
                               prompt=self.prompt)
        response, token_usage = qa(question, history=history, return_usage=return_usage)
        self.token_usage.extend(token_usage)
        if return_usage:
            return response, self.token_usage
        else:
            return response


    def prepare_retrivers(self, 
                          **kwargs: Any) -> None:
        """
        Prepare the retrievers for the retrieval process.
        """

        vectordb = VectorDB(
            model_name="",
            embedding_model="BAAI/bge-small-en-v1.5" 
        )   
        vectordb.load_local()
        len_k = 5
        default_retriever = vectordb.as_retriever(
            search_type="similarity", search_kwargs={'k': len_k, 'fetch_k': 5*len_k })
        self.ensemble_retriever = default_retriever

