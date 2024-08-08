import os
from dotenv import load_dotenv
from langchain_core.callbacks import CallbackManagerForChainRun
from langchain.chains.retrieval_qa.base import RetrievalQA

from telemedicine.core.base import Usage, openai_chat
from telemedicine.core.g_search import GoogleSearchTool
from telemedicine.core.prompt_template import standalone_question_from_history


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
        if self.retriever is not None:
            self.qa = RetrievalQA.from_chain_type(
                    llm=self.llm, retriever=self.retriever, **self.kwargs
                )
        try:
            load_dotenv('.env')
            self.api_key = os.getenv('OPENAI_API_KEY')
        except Exception as e:
            raise ValueError(f"Please set the openai_key in env file. Error: {str(e)}")
        self.model = "llama3-8b-8192"
        self.token_usage = []

    def __call__(self, question, history=None, return_usage=True):
        if history:
            standalone_question = self.question_from_history(question, history)
            print(f"Standalone question: {standalone_question}")

        clean_docs = []
        # if history:
        #     clean_docs += GoogleSearchTool(standalone_question).result()
        # else:
        #     clean_docs += GoogleSearchTool(question).result()
        if self.retriever is not None:
            _run_manager = CallbackManagerForChainRun.get_noop_manager()
            if history:
                docs = self.qa._get_docs(standalone_question, run_manager=_run_manager)
            else:
                docs = self.qa._get_docs(question, run_manager=_run_manager)
            _clean_docs = [doc.page_content for doc in docs]   
            clean_docs += _clean_docs
        if history:
            question = self.combine_questions(question, standalone_question)
        final_prompt = self.prompt.template.replace("{context}", "\n".join(clean_docs))
        final_prompt = final_prompt.replace("{question}", question)
        response, token_usage = openai_chat(
            question=final_prompt,
            system_message=self.system_prompt, 
            model=self.model, 
            max_tokens=4096, 
            temperature=0.25,
            return_usage=True
        )
        self.token_usage.append(token_usage)
        if return_usage:
            return response, self.token_usage
        else:
            return response
    
    def combine_questions(self, question1, question2):
        prompt = f"{question1}\nStandalone question based on history: {question2}"
        return prompt
    
    def question_from_history(self, question, history):
        prompt = standalone_question_from_history(question, history)
        response, token_usage = openai_chat(
            question=prompt,
            model="gpt-4o-mini-2024-07-18", 
            max_tokens=4096, 
            temperature=0.5,
            return_usage=True   
        )
        self.token_usage.append(token_usage)
        return response