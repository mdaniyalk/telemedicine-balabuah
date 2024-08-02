import os
from dotenv import load_dotenv
from langchain_community.utilities.google_search import GoogleSearchAPIWrapper
from langchain_core.documents import Document
from langchain_community.document_transformers.html2text import Html2TextTransformer
import requests
from bs4 import BeautifulSoup

from scipy.spatial.distance import cdist
from telemedicine.core.embedding import get_embeddings


from telemedicine.core.text_splitter import RecursiveTokenTextSplitter
from telemedicine.core.thread import multithreading


def calculate_similarity(embedding1, embedding2):
    return 1 - cdist([embedding1], [embedding2], metric='cosine')

def google_search(question):
    tool = GoogleSearchTool(question)
    doc_result = tool.result()
    result = ''
    for doc in doc_result:
        result+=f"{doc}\n"
    return result


class GoogleSearchTool:
    def __init__(self, question, num_results=2):
        load_dotenv('.env')
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.google_cse_id = os.getenv('GOOGLE_CSE_ID')
        self.search = GoogleSearchAPIWrapper(google_api_key=self.google_api_key, 
                                            google_cse_id=self.google_cse_id, 
                                            k=5)
        self.num_results = num_results
        self.question = question
        self.question_embedding = get_embeddings(question)
    
    def result(self):
        results = self.search.results(self.question, num_results=5*self.num_results)
        for res in results:
            _doc_result = self._process_result(res)
            if _doc_result is not None:
                break
        doc_result = []
        for doc in _doc_result:
            doc_result.append(doc)
        print('doc_result:', doc_result)
        return doc_result

    def _process_result(self, result):
        try:
            html_doc = requests.get(result['link'])
            soup = BeautifulSoup(html_doc.text, 'html.parser')
            _txt = soup.get_text()
            _txt = ' '.join(_txt.split())
            if "cloudfront" in _txt.lower() or "error" in _txt.lower():
                return None
            doc = Document(page_content=_txt)
            text_splitter = RecursiveTokenTextSplitter(
                chunk_size = 750, chunk_overlap = 10
            )
            _splitted = text_splitter.split_documents([doc])
            _splitted = [split.page_content for split in _splitted]
            results = _splitted[0:1]
            # embeddings = multithreading(get_embeddings, _splitted)
            # sim_score = [calculate_similarity(self.question_embedding, _embeddings) for _embeddings in embeddings]
            # top_3_indices = sorted(range(len(sim_score)), key=lambda i: sim_score[i], reverse=True)[:3]
            # results = [_splitted[i] for i in top_3_indices]
            return results
        except:
            return None