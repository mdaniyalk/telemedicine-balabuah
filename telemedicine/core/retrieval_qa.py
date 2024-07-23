import os
import urllib.parse
import numpy as np
from fuzzywuzzy import fuzz
from copy import copy
from langchain_core.callbacks import CallbackManagerForChainRun

from rag.core.base import openai_chat
from rag.core.configuration import Configuration
from rag.core.langchain import RetrievalQA
from rag.core.math_utils import cosine_similarity
from rag.core.prompt_template import standalone_question_from_history
from rag.core.thread import multithreading


class CustomRetrievalQA:
    def __init__(self, llm, retriever, prompt, system_prompt=None, **kwargs):
        self.llm = llm
        self.retriever = retriever
        self.prompt = prompt
        self.system_prompt = system_prompt
        self.kwargs = kwargs
        if 'chain_type' not in self.kwargs:
            self.kwargs['chain_type'] = 'stuff'
        if 'chain_type_kwargs' not in self.kwargs:
            self.kwargs['chain_type_kwargs'] = {"prompt": self.prompt}
        if isinstance(self.retriever, list):
            qa = []
            for i, r in enumerate(self.retriever):
                qa.append(RetrievalQA.from_chain_type(
                    llm=copy(self.llm), retriever=r, **copy(self.kwargs)
                ))
            self.qa = qa
            self.multi_documents = True
        else:
            self.qa = RetrievalQA.from_chain_type(
                llm=self.llm, retriever=self.retriever, **self.kwargs
            )
            self.multi_documents = False
        config = Configuration.load('config.toml')
        
        try:
            self.api_key = config.get('openai_key')
        except Exception as e:
            raise ValueError(f"Please set the openai_key in config.toml file. Error: {str(e)}") from e
        try:
            self.openai_main_model = config.get('openai_main_model')
        except Exception as e:
            raise ValueError(f"Please set the openai_main_model in config.toml file. Error: {str(e)}") from e
        try:
            self.openai_organization = config.get('openai_organization')
        except Exception as e:
            raise ValueError(f"Please set the openai_organization in config.toml file. Error: {str(e)}") from e
        try:
            self.base_url = config.get('openai_base_url')
        except Exception as e:
            raise ValueError(f"Please set the openai_base_url in config.toml file. Error: {str(e)}") from e
    
    def __call__(self, question, history=None):
        if history:
            standalone_question = self.question_from_history(question, history)
        
        if self.multi_documents:
            def get_multi_doc_wrapper(x):
                docs = x._get_docs(
                    question, run_manager=CallbackManagerForChainRun.get_noop_manager()
                )
                if history:
                    docs += x._get_docs(
                        standalone_question, run_manager=CallbackManagerForChainRun.get_noop_manager()
                    )
                return docs
            res = multithreading(get_multi_doc_wrapper, self.qa)
            group_documents = [
                {
                    "documents": docs,
                    "source": docs[0].metadata.get('url') if docs[0].metadata.get('url') is not None else docs[0].metadata.get('source')
                }
                for docs in res
            ]
            documents, sources = self.prepare_multi_documents(group_documents)
            final_prompt = self.prompt.template.replace("{context}", documents)
            final_prompt = final_prompt.replace("{doc_references}", sources)
        else:
            _run_manager = CallbackManagerForChainRun.get_noop_manager()
            docs = self.qa._get_docs(question, run_manager=_run_manager)
            if history:
                docs += self.qa._get_docs(standalone_question, run_manager=_run_manager)
            docs = self.remove_duplicate_documents(docs)
            clean_docs = [doc.page_content for doc in docs]
            source_doc = docs[0].metadata.get('url') if docs[0].metadata.get('url') is not None else docs[0].metadata.get('source')
            final_prompt = self.prompt.template.replace("{context}", "\n".join(clean_docs))
            final_prompt = final_prompt.replace("{doc_references}", self.get_reference_document(source_doc))
        if history:
            question = self.combine_questions(question, standalone_question)
        final_prompt = final_prompt.replace("{question}", question)
        
        print('final_prompt', final_prompt)
        response = openai_chat(
            question=final_prompt,
            system_message=self.system_prompt, 
            api_key=self.api_key,
            organization = self.openai_organization,
            base_url = self.base_url,
            model=self.openai_main_model, 
            max_tokens=4096, 
            temperature=0.1
        )
        print('response', response)
        return response
    
    def get_reference_document(self, file_path):
        if "http" in file_path:
            return f"{file_path}"
        filename = os.path.basename(file_path)
        file_url = "file://" + file_path
        print('file_url', file_url)
        return f"[{filename}]({file_url})"

    def question_from_history(self, question, history):
        prompt = standalone_question_from_history(question, history)
        response = openai_chat(
            question=prompt,
            api_key=self.api_key,
            organization = self.openai_organization,
            base_url = self.base_url,
            model=self.openai_main_model, 
            max_tokens=4096, 
            temperature=0.5
        )
        return response
    
    def combine_questions(self, question1, question2):
        prompt = f"{question1}\nStandalone question based on history: {question2}"
        return prompt
    
    def remove_duplicate_documents(self, documents):
        similarity_threshold = 80
        unique_docs = []
        
        for obj in documents:
            is_duplicate = False
            
            if len(unique_docs) > 0:
                for seen_doc in unique_docs:
                    similarities = fuzz.partial_ratio(obj.page_content, seen_doc.page_content)
                    if similarities > similarity_threshold:
                        is_duplicate = True
            
            if not is_duplicate:
                unique_docs.append(obj)
        
        return unique_docs
    
    def prepare_multi_documents(self, group_documents):
        documents = ''
        sources = ''
        for i, docs in enumerate(group_documents):
            if len(docs['documents']) == 0:
                continue
            
            _docs = self.remove_duplicate_documents(docs['documents'])
            # _docs = docs['documents']
            clean_docs = [doc.page_content for doc in _docs]
            _documents = "\n".join(clean_docs)
            _documents += "\n\n"
            _source = self.get_reference_document(docs['source'])
            sources += f'doc_{i}: {_source}\n'
            _documents = f'{_source}:\n' + _documents
            documents += _documents
        return documents, sources
            

