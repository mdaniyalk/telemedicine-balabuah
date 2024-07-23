"Module for document or text splitting."
from typing import (
    Any,
    Iterable,
    List,
    Optional,
)

import tiktoken
from tqdm import tqdm

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from telemedicine.core.thread import multithreading


class RecursiveTokenTextSplitter(RecursiveCharacterTextSplitter):
    """Customized RecursiveTokenTextSplitter. 
    Inherits from langchain_text_splitters.RecursiveCharacterTextSplitter.
    """
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._length_function = self._get_len_function()

    def create_documents(self, 
                         texts: List[str], 
                         metadatas: Optional[List[dict]] = None
                         ) -> List[Document]:
        """Create documents from a list of texts."""
        _metadatas = metadatas or [{}] * len(texts)
        doc_index = range(len(texts))
        docs = multithreading(self._create_documents, texts, _metadatas, doc_index)
        documents = []
        for doc in docs:
            documents += doc
        return documents

    def split_documents(self, documents: Iterable[Document]) -> List[Document]:
        """Split documents."""
        texts, metadatas = [], []
        for doc in tqdm(documents, desc='Splitting documents'):
            texts.append(doc.page_content)
            metadatas.append(doc.metadata)
        return self.create_documents(texts, metadatas=metadatas)
    
    def _create_documents(self, text, metadata, doc_index):
        """
        Create documents from a chunk of text. 
        Wrapper for the original create_documents method.
        """
        documents = []
        index = 0
        previous_chunk_len = 0
        splitted_text = self.split_text(text)
        if len(splitted_text) > 0:
            for chunk in tqdm(splitted_text, desc=f'Splitting text. Doc: {doc_index}'):
                if self._add_start_index:
                    offset = index + previous_chunk_len - self._chunk_overlap
                    index = text.find(chunk, max(0, offset))
                    metadata["start_index"] = index
                    previous_chunk_len = len(chunk)
                new_doc = Document(page_content=chunk, metadata=metadata)
                documents.append(new_doc)
        return documents
    
    def _get_len_function(self):
        enc = tiktoken.get_encoding('cl100k_base')

        def _tiktoken_encoder(text: str) -> int:
            return len(
                enc.encode(text)
            )
        return _tiktoken_encoder