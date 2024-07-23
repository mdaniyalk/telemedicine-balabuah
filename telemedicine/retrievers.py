import os
from typing import Any, Dict, List, Tuple
import json

from telemedicine.core import (
    calculate_similarity, 
    openai_chat, 
    openai_embedding, 
    BaseRetrievers,
    CustomEnsembleRetriever
)
from telemedicine.core.configuration import Configuration
from telemedicine.core.directory_utilities import validate_path
from telemedicine.core.langchain import (
    ChatOpenAI,
    MultiQueryRetriever,
    set_debug
)
from telemedicine.core.vectorstore import VectorDB
from telemedicine.core.prompt_template import (
    multi_query_retriver_prompt,
    retrieval_qa_prompt
)
from telemedicine.core.retrieval_qa import CustomRetrievalQA


set_debug(True)

class RetrieveFromDocuments(BaseRetrievers):
    """
    Class to retrieve information from documents using a retrieval QA system.
    """

    def __init__(self, config: Configuration = None, **kwargs) -> None:
        super().__init__(config)

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
        self.prepare_retrivers(question=question, **kwargs)
        self.prompt = retrieval_qa_prompt()
        llm = ChatOpenAI(model_name=self.config('openai_main_model'),
                         max_tokens=4096,  
                         openai_api_key=self.config('openai_key'), 
                         openai_organization=self.config('openai_organization'),
                         openai_api_base=self.config('openai_base_url'),
                         temperature=0.05)
        qa = CustomRetrievalQA(llm=llm, 
                               retriever=self.ensemble_retriever, 
                               prompt=self.prompt)
        response = qa(question, history=history)
        print(response)
        return response


    def prepare_retrivers(self, 
                          question: str,
                          db_folder_paths: List[str]=None, 
                          vectordbs: List[VectorDB]=None,
                          **kwargs: Any) -> None:
        """
        Prepare the retrievers for the retrieval process.

        Args:
            db_folder_paths (List[str]): List of folder paths for vector databases.
            vectordbs (List[VectorDB]): List of VectorDB objects.
        """
        self.db_folder_paths = db_folder_paths
        self.vectordbs = vectordbs
        if self.db_folder_paths is None and self.vectordbs is None:
            raise ValueError("Either db_folder_paths or vectordbs must be provided.") 


        reference_document_title = []
        retrievers = []
        len_data = len(vectordbs) if vectordbs is not None else len(db_folder_paths)
        for i in range(len_data):
            if vectordbs is not None:
                vectordb = vectordbs[i]
            else:
                vectordb = VectorDB(embedding_model=self.config('openai_embedding_model'),
                                    openai_api_key=self.config('openai_key'))
                path = db_folder_paths[i]
                path = validate_path(path, level='final')
                vectordb.load_local(db_folder_paths[i])
            len_k = 3 - len_data
            len_k = max([2, len_k])
            llm = ChatOpenAI(temperature=0.1, 
                             openai_api_key=self.config('openai_key'), 
                             openai_organization=self.config('openai_organization'),
                             openai_api_base=self.config('openai_base_url'),
                             max_tokens=2048, 
                             model_name=self.config('openai_main_model'))
            summary = vectordb.get_document_summary()
            multi_query_prompt = multi_query_retriver_prompt(summary['text'])
            multi_query_retriver = MultiQueryRetriever.from_llm(
                retriever=vectordb.as_retriever(search_type="mmr", 
                                                search_kwargs={
                                                    'k': len_k, 
                                                    'fetch_k': 5*len_k,
                                                }), 
                llm=llm,
                prompt=multi_query_prompt
            )

            faiss_retriever = vectordb.as_retriever(search_type="mmr", 
                                                    search_kwargs={
                                                        'k': len_k, 
                                                        'fetch_k': 5*len_k,
                                                    })
            retrievers += [multi_query_retriver, faiss_retriever]
            reference_document_title.extend(vectordb.title)
        retrievers_weights = [1/(len(retrievers)) for _ in range(len(retrievers))]
        ensemble_retriever = CustomEnsembleRetriever(
            retrievers=retrievers, weights=retrievers_weights
        )
        self.ensemble_retriever = ensemble_retriever
        self.reference_document_title = reference_document_title

