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
from telemedicine.core.retrieval_qa import CustomRetrievalQA


set_debug(True)

class Retrieval(BaseRetrievers):
    """
    Class to retrieve information from documents using a retrieval QA system.
    """

    def __init__(self, **kwargs) -> None:
        self.prompt = retrieval_qa_prompt()
        self.llm = ChatOpenAI(
            model_name='llama3-8b-8192',
            max_tokens=4096,  
            openai_api_key=os.getenv('GROQ_API_KEY'), 
            openai_api_base="https://api.groq.com/openai/v1",
            temperature=0.1
        )

    def result(self, 
               question: str,
               history: str = None,
               **kwargs: Any) -> str:
        """
        Retrieve the result for a given question.

        Args:
            question (str): The question to retrieve the result for.
            history (str): The history of interactions.

        Returns:
            The result of the retrieval process as a string.
        """
        # self.prepare_retrivers(question=question, **kwargs)
        self.ensemble_retriever = None
        qa = CustomRetrievalQA(llm=self.llm, 
                               retriever=self.ensemble_retriever, 
                               prompt=self.prompt)
        response = qa(question, history=history)
        return response


    # def prepare_retrivers(self, 
    #                       question: str,
    #                       **kwargs: Any) -> None:
    #     """
    #     Prepare the retrievers for the retrieval process.

    #     Args:
    #         db_folder_paths (List[str]): List of folder paths for vector databases.
    #         vectordbs (List[VectorDB]): List of VectorDB objects.
    #     """

    #     vectordb = VectorDB(embedding_model="text-embedding-3-small",
    #                         openai_api_key=os.getenv('OPENAI_API_KEY'))
    #     vectordb.load_local()
    #     len_k = 3
    #     llm = ChatOpenAI(
    #         model_name='llama3-8b-8192',
    #         max_tokens=2048,  
    #         openai_api_key=os.getenv('GROQ_API_KEY'), 
    #         openai_api_base="https://api.groq.com/openai/v1",
    #         temperature=0.1
    #     )
    #     multi_query_prompt = multi_query_retriver_prompt()
    #     multi_query_retriver = MultiQueryRetriever.from_llm(
    #         retriever=vectordb.as_retriever(search_type="mmr", 
    #                                         search_kwargs={
    #                                             'k': len_k, 
    #                                             'fetch_k': 5*len_k,
    #                                         }), 
    #         llm=llm,
    #         prompt=multi_query_prompt
    #     )

    #     faiss_retriever = vectordb.as_retriever(search_type="mmr", 
    #                                             search_kwargs={
    #                                                 'k': len_k, 
    #                                                 'fetch_k': 5*len_k,
    #                                             })
    #     retrievers += [multi_query_retriver, faiss_retriever]
    #     reference_document_title.extend(vectordb.title)
    #     retrievers_weights = [1/(len(retrievers)) for _ in range(len(retrievers))]
    #     ensemble_retriever = CustomEnsembleRetriever(
    #         retrievers=retrievers, weights=retrievers_weights
    #     )
    #     self.ensemble_retriever = ensemble_retriever
    #     self.reference_document_title = reference_document_title

