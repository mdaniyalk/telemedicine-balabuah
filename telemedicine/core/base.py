"Module for base functionalities."
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv
import os
from typing import Any, List, Optional
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cdist


@retry(wait=wait_random_exponential(multiplier=0.5, max=5), stop=stop_after_attempt(3))
def openai_chat(question, 
                system_message: Optional[str] = None, 
                model: Optional[str] = None, 
                api_key: Optional[str] = None, 
                history: Optional[str] = None, 
                return_usage: Optional[bool] = False,
                **kwargs) -> str:
    """
    Function to interact with OpenAI chat API.
    
    Args:
        question (str): The user's question.
        system_message (str): The system's message.
        model (str): The model to use.
        api_key (str): The API key for authentication.
    
    Returns:
        str: The response message from the chat.
    """
    load_dotenv(".env")
    if api_key is None:
        try:
            openai_api_key = os.getenv('OPENAI_API_KEY')
        except Exception as e:
            raise ValueError("Please set the api_key in the params or on the environment variable.")
    else:
        openai_api_key = api_key

    if model is None:
        raise ValueError("Please set the model name in the params.")
        
    if system_message is None:
        system_message = "You are a helpful assistant."
        print("Please set the params system_message.")
        print('Using default system message of "You are a helpful assistant.".')
    
    messages = [{"role": "system", "content": system_message}]
    if history is not None:
        messages.append({"role": "user", "content": f"Chat History: {history}"})
    messages.append({"role": "user", "content": question})
    if model == "llama3-8b-8192":
        not_complete = True
        while not_complete:
            try:
                client, model_id = groq_wrapper()
                model_id = f"{model}-{model_id}"
                completion = client.chat.completions.create(
                    model=model,
                    seed=42,
                    messages=messages,
                    **kwargs
                )
                not_complete = False
            except:
                continue
    else:
        client = OpenAI(
            api_key=openai_api_key
        )
        model_id = f"{model}"
        completion = client.chat.completions.create(
            model=model,
            seed=42,
            messages=messages,
            **kwargs
        )

    response_content = completion.choices[0].message.content
    if return_usage:
        prompt_tokens = completion.usage.prompt_tokens
        completion_tokens = completion.usage.completion_tokens
        total_tokens = completion.usage.total_tokens
        usage = Usage(
            prompt_tokens = prompt_tokens, completion_tokens = completion_tokens, total_tokens = total_tokens, model_name = model_id
        )
        return response_content, usage
    else:
        return response_content

def groq_wrapper():
    """
    Wrapper function to replace OpenAI with Groq API.
    """
    import random
    load_dotenv(".env")
    a = random.randint(1, 100)
    b = random.randint(1, 100)
    i = random.randint(a, a*b) % 5
    api_key = os.getenv(f'GROQ_API_KEY_{i}')
    print(f"Using Groq API Key {i}")
    client = OpenAI(
        api_key=api_key, 
        base_url='https://api.groq.com/openai/v1',
    )
    model_id = i
    return client, model_id


@retry(wait=wait_random_exponential(multiplier=0.5, max=5), stop=stop_after_attempt(3))
def openai_embedding(text, 
                     model: Optional[str] = None, 
                     api_key: Optional[str] = None,
                     return_usage: Optional[bool] = False,
                     **kwargs) -> List[float]:
    """
    Function to interact with OpenAI embedding API.
    
    Args:
        text (str): The text to embed.
        model (str): The model to use (default is "text-embedding-3-small").
        api_key (str): The API key for authentication.
    
    Returns:
        str: The embedding of the text.
    """
    load_dotenv(".env")
    if api_key is None:
        try:
            openai_api_key = os.getenv('OPENAI_API_KEY')
        except Exception as e:
            raise ValueError("Please set the api_key in the params or on the environment variable.")
    else:
        openai_api_key = api_key
    if model is None:
        raise ValueError("Please set the model name in the params.")
    
    client = OpenAI(
        api_key=openai_api_key
    )
    embedding = client.embeddings.create(
        model=model,
        input=[text],
        **kwargs
    )

    response_content = embedding.data[0].embedding
    if return_usage:
        prompt_tokens = embedding.usage.prompt_tokens
        total_tokens = embedding.usage.total_tokens
        usage = Usage(
            prompt_tokens = prompt_tokens, completion_tokens = 0, total_tokens = total_tokens, model_name = model
        )
        return response_content, usage
    else:
        return response_content

    
def calculate_similarity(embedding1, embedding2, mode='sklearn'):
    """
    Calculate the cosine similarity between two embeddings.

    Args:
        embedding1: The first embedding.
        embedding2: The second embedding.

    Returns:
        float: The cosine similarity between the two embeddings.
    """
    if mode == 'sklearn':
        return cosine_similarity([embedding1], [embedding2])[0][0]
    else:
        return 1 - cdist([embedding1], [embedding2], metric='cosine')

@dataclass
class Usage:
    """
    Base Usage Class.
    """
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    model_name: str = None

    def add(self, prompt_tokens=None, completion_tokens=None, total_tokens=None, usage_tokens=None):
        if usage_tokens is None:
            if prompt_tokens is None and completion_tokens is None and total_tokens is None:
                raise ValueError("At least one of 'prompt_tokens', 'completion_tokens', 'total_tokens', or 'tokens' must be provided.")
            else:
                self.prompt_tokens += prompt_tokens
                self.completion_tokens += completion_tokens
                self.total_tokens += total_tokens
        elif isinstance(usage_tokens, Usage):
            self.prompt_tokens += usage_tokens.prompt_tokens
            self.completion_tokens += usage_tokens.completion_tokens
            self.total_tokens += usage_tokens.total_tokens

@dataclass
class Message:
    """
    Base Message Class in a chat.
    """
    message_id: str
    conversation_index: int
    timestamp: datetime
    message_type: str
    message_str: str
    
    def get_dict(self) -> dict[str, str]:
        """
        Get the dict representation of the message.
        
        Returns:
            dict: The dict representation of the message.
        """
        timestamp_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return {
            "message_id": self.message_id,
            "conversation_index": self.conversation_index,
            "timestamp": timestamp_str,
            "message_type": self.message_type,
            "message_str": self.message_str
        }

    def get_message_dialogue(self) -> str:
        """
        Get the message string.
        
        Returns:
            str: The message string.
        """
        dialog = f"{self.message_type}: {self.message_str}"
        return dialog
    
    @classmethod
    def load_from_dict(cls, data: dict[str, Any]) -> 'Message':
        """
        Load a Message object from a dictionary.
        
        Args:
            data (dict): The dictionary containing the message data.
        
        Returns:
            Message: The Message object.
        """
        if isinstance(data["timestamp"], str):
            timestamp = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
        else:
            timestamp = data["timestamp"]
        return cls(
            message_id=data["message_id"],
            conversation_index=data["conversation_index"],
            timestamp=timestamp,
            message_type=data["message_type"],
            message_str=data["message_str"]
        )
    



class BaseRetrievers(ABC):
    """
    Base class for retrievers.

    Attributes:
        config (Configuration): The configuration settings.
    """
    
    def __init__(self):
        self.token_usage = []

    @classmethod
    def retrieve(cls,
                 **kwargs):
        """
        Retrieve method to instantiate the class and call the result method.

        Args:
            **kwargs: Keyword arguments.

        Returns:
            The result of the retrieved document.
        """
        return cls(**kwargs).result(**kwargs)
    
    @abstractmethod
    def result(self, 
               question: Any, 
               history: str = None) -> None:
        """
        Abstract method to be implemented by subclasses.

        Args:
            question (str): The question to retrieve results for.
            history (str): The history of interactions.

        Returns:
        The result of the retrieval.
        """
        pass

