"""
Ensemble retriever that ensemble the results of 
multiple retrievers by using weighted  Reciprocal Rank Fusion
"""
from typing import Any, Dict, List, Optional, cast

from langchain_core.callbacks import (
    CallbackManagerForRetrieverRun,
)
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.config import patch_config

from langchain_core.documents import Document
from langchain.retrievers import EnsembleRetriever
from telemedicine.core.thread import multithreading


class CustomEnsembleRetriever(EnsembleRetriever):
    """
    Custom ensemble retriver that leverage multithreading.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def rank_fusion(
        self,
        query: str,
        run_manager: CallbackManagerForRetrieverRun,
        *,
        config: Optional[RunnableConfig] = None,
    ) -> List[Document]:
        """
        Retrieve the results of the retrievers and use rank_fusion_func to get
        the final result.

        Args:
            query: The query to search for.

        Returns:
            A list of reranked documents.
        """
        def invoke_retriever(i, retriever):
            return retriever.invoke(
                query,
                patch_config(
                    config, callbacks=run_manager.get_child(tag=f"retriever_{i+1}")
                ),
            )

        # Get the results of all retrievers.
        retriever_docs = multithreading(invoke_retriever, 
                                        range(len(self.retrievers)), 
                                        self.retrievers)

        # Enforce that retrieved docs are Documents for each list in retriever_docs
        retriever_docs = [
            [Document(page_content=cast(str, doc)) if isinstance(doc, str) else doc for doc in doc_list]
            for doc_list in retriever_docs
        ]


        # apply rank fusion
        fused_documents = self.weighted_reciprocal_rank(retriever_docs)

        return fused_documents

    def weighted_reciprocal_rank(
        self, doc_lists: List[List[Document]]
    ) -> List[Document]:
        
        if len(doc_lists) != len(self.weights):
            raise ValueError(
                "Number of rank lists must be equal to the number of weights."
            )

        # Create a union of all unique documents in the input doc_lists
        all_documents = {doc.page_content for doc_list in doc_lists for doc in doc_list}
    

        # Initialize the RRF score dictionary for each document
        rrf_score_dic = {doc: 0.0 for doc in all_documents}

        # Calculate RRF scores for each document
        for doc_list, weight in zip(doc_lists, self.weights):
            for rank, doc in enumerate(doc_list, start=1):
                rrf_score = weight * (1 / (rank + self.c))
                rrf_score_dic[doc.page_content] += rrf_score

        # Sort documents by their RRF scores in descending order
        sorted_documents = sorted(
            rrf_score_dic.keys(), key=lambda x: rrf_score_dic[x], reverse=True
        )

        # Map the sorted page_content back to the original document objects
        page_content_to_doc_map = {
            doc.page_content: doc for doc_list in doc_lists for doc in doc_list
        }
        sorted_docs = [
            page_content_to_doc_map[page_content] for page_content in sorted_documents
        ]

        return sorted_docs
