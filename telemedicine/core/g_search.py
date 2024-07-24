import os
from dotenv import load_dotenv
from langchain_community.utilities.google_search import GoogleSearchAPIWrapper
from langchain.tools import Tool


def google_search(question, mode='search'):
    """
    Perform a Google search for the given question.

    This function initializes and configures the Google Search API by providing the necessary parameters:
    - `api_key`: List containing Google API key and custom search engine (CSE) ID for API initialization.
    - `question`: The search query/question.

    The function utilizes the GoogleSearchAPIWrapper class to create a search function for Google.
    It sets up the connection to the Google Search API using the specified API key and CSE ID.

    Parameters:
    - `question` (str): The search query/question.
    - `api_key` (list, optional): List containing Google API key and custom search engine (CSE) ID for API initialization. 
      Default is None.

    Returns:
    - `result` (list): List of search results obtained from the Google Search API.

    Example usage:
    api_key = ['YOUR_GOOGLE_API_KEY', 'YOUR_CUSTOM_SEARCH_ENGINE_ID']
    search_result = google_search(question="How does photosynthesis work?", api_key=api_key)
    """

    load_dotenv('.env')
    google_api_key = os.getenv('google_api_key')
    google_cse_id = os.getenv('google_cse_id')
    search = GoogleSearchAPIWrapper(google_api_key=google_api_key, 
                                    google_cse_id=google_cse_id, 
                                    k=5)
    if mode == 'search':
        tool = Tool(
            name="Google Search",
            description="Search Google for recent results.",
            func=search.run,
        )
        result = tool.run(question)
    elif mode == 'link':
        res = search.results(question, num_results=3)
        result = ''
        for _res in res:
            try:
                result+=f"- [{_res['title']}]({_res['link']})\n"
            except Exception as _:
                result += ''
    return result