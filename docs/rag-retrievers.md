# telemedicine.retrievers
Module that handle the agent to LLM interaction

---
## RetrieveFromDocuments
```python
class telemedicine.retrievers.RetrieveFromDocuments(openai_api_key, openai_base_url=None, openai_organization=None, openai_proxy=None, **kwargs)
```
Class to retrieve information from documents using a retrieval QA system.

Inherits from [`class telemedicine.core.base.BaseRetrievers()`](rag-core?id=ragcore)

---
**Parameters**

- **openai_api_key** (str)

    The OpenAI API key.

- **openai_base_url** (str, optional)
    
    The base URL for the OpenAI API. Defaults to None.

- **openai_organization** (str, optional)

    The OpenAI organization ID. Defaults to None.

- **openai_proxy** (str, optional)

    The proxy to be used for connecting to the OpenAI API. Defaults to None.


---
**Attributes:**

- **openai_main_model**: `str`

    The main OpenAI model to be used for retrieval.
- **openai_tertiary_model**: `str`

    The tertiary OpenAI model to be used for retrieval.
- **openai_embedding_model**: `str`

    The OpenAI embedding model to be used for embedding documents.
- **db_folder_paths**: `List[str]`

    List of folder paths for vector databases.
- **vectordbs**: `List[VectorDB]`

    List of VectorDB objects.
- **prompt**: `str`

    The prompt used for retrieval.
- **reference_document_title**: `List[str]`

    The titles of the reference documents.
- **ensemble_retriever**: `CustomEnsembleRetriever`

    An ensemble retriever object that combines multiple retrievers.

---
**Methods**

```python
result(question, history=None, **kwargs)
```
Retrieve the result for a given question.

Parameters:
- question (str)

    The question to retrieve the result for.

- history (str)
    
    The history of interactions.

Returns:
- str: The result of the retrieval process as a string.

---
```python
prepare_retrivers(question, db_folder_paths=None,  vectordbs=None, **kwargs)
```
Prepare the retrievers for the retrieval process.

Parameters:
- question (str)

    The question to retrieve the result for.

- db_folder_paths (List[str], optional)

    List of folder paths for vector databases. Defaults to None.

- vectordbs (List[[VectorDB](rag-core?idvectordb)], optional)

    List of VectorDB objects. Defaults to None.

Returns:
- None: This method modifies the instance attributes directly.

---

## RetrieveDetailQuestion
```python
class telemedicine.retrievers.RetrieveDetailQuestion(openai_api_key, openai_base_url=None, openai_organization=None, openai_proxy=None, **kwargs)
```
Class to retrieve detailed questions from the user.

Inherits from [`class telemedicine.core.base.BaseRetrievers()`](rag-core?id=ragcore)

---
**Parameters**

- **openai_api_key** (str)

    The OpenAI API key.

- **openai_base_url** (str, optional)
    
    The base URL for the OpenAI API. Defaults to None.

- **openai_organization** (str, optional)

    The OpenAI organization ID. Defaults to None.

- **openai_proxy** (str, optional)

    The proxy to be used for connecting to the OpenAI API. Defaults to None.


---
**Attributes:**

- **openai_main_model**: `str`

    The main OpenAI model to be used for retrieval.

---
**Methods**

```python
result(question, history=None, **kwargs)
```
Retrieve the result for a given question.

Parameters:
- question (str)

    The current question to then asked more

- history (str)
    
    The history of interactions.

Returns:
- Dict[str, Any]: A dictionary containing the response.

---

## RetrieveDocuments
```python
class telemedicine.retrievers.RetrieveDocuments(openai_api_key, openai_base_url=None, openai_organization=None, openai_proxy=None, **kwargs)
```
Class to retrieve documents based on a refined question.

Inherits from [`class telemedicine.core.base.BaseRetrievers()`](rag-core?id=ragcore)

---
**Parameters**

- **openai_api_key** (str)

    The OpenAI API key.

- **openai_base_url** (str, optional)
    
    The base URL for the OpenAI API. Defaults to None.

- **openai_organization** (str, optional)

    The OpenAI organization ID. Defaults to None.

- **openai_proxy** (str, optional)

    The proxy to be used for connecting to the OpenAI API. Defaults to None.


---
**Attributes:**

- **openai_main_model**: `str`

    The main OpenAI model to be used for retrieval.
- **openai_embedding_model**: `str`

    The OpenAI embedding model to be used for embedding documents.
- **target_folder**: `str`

    Target folder paths for vector databases.

---
**Methods**

```python
result(question, history=None, **kwargs)
```
Retrieve the result for a given question.

Parameters:
- question (Dict[str, Any])

    The refined question to retrieve documents for.

- history (str)
    
    The history of interactions.

Returns:
- Tuple[Any, Any]: A tuple containing vector databases and their paths.

---
```python
calculate_similarity(embedding_question, vectorstores)
```
Prepare the retrievers for the retrieval process.

Parameters:
- embedding_question (List[float]): 

    The question to retrieve the result for.

- vectorstores (List[Dict[str, Any]]):

    List of vector stores.

Returns:
- Tuple[List[float], List[Dict[str, Any]]]: A tuple containing the similarities and updated vector stores.

---

## RetrieveFinalDocuments
```python
class telemedicine.retrievers.RetrieveFinalDocuments(openai_api_key, openai_base_url=None, openai_organization=None, openai_proxy=None, **kwargs)
```
Class to retrieve final documents based on a refined question.

Inherits from [`class telemedicine.core.base.BaseRetrievers()`](rag-core?id=ragcore)

---
**Parameters**

- **openai_api_key** (str)

    The OpenAI API key.

- **openai_base_url** (str, optional)
    
    The base URL for the OpenAI API. Defaults to None.

- **openai_organization** (str, optional)

    The OpenAI organization ID. Defaults to None.

- **openai_proxy** (str, optional)

    The proxy to be used for connecting to the OpenAI API. Defaults to None.


---
**Attributes:**

- **openai_main_model**: `str`

    The main OpenAI model to be used for retrieval.
- **openai_embedding_model**: `str`

    The OpenAI embedding model to be used for embedding documents.
- **target_folder**: `str`

    Target folder paths for vector databases.

---
**Methods**

```python
result(question, document_candidates, root_document_path, history=None, **kwargs)
```
Retrieve the result for a given question.

Parameters:
- question (str)

    The question to retrieve the result for.

- document_candidates (List[str])
    
    The list of document candidates.

- root_document_path (str)
    
    The root path for the documents.

- history (str)
    
    The history of interactions.

Returns:
- Tuple[bool, Any]: A tuple containing the status and the retrieved documents or response.

---

## formattedTag_filter
```python
function telemedicine.retrievers.formattedTag_filter(query=None, query_embedding=None, formattedTag=None, formattedTagEmbedding=None, threshold=0.25)
```
Function to filter tags based on their similarity to a query or query embedding.


---
**Parameters**

- **query** (str, optional)

    The query string. Defaults to None.

- **query_embedding** (List[float], optional)
    
    The embedding of the query. Defaults to None.

- **formattedTag** (str, optional)

    The formatted tag string. Defaults to None.

- **formattedTagEmbedding** (List[float], optional)

    The embedding of the formatted tag. Defaults to None.

- **threshold** (float, optional)

    The similarity threshold for filtering. Defaults to 0.25.

---
**Returns**
- bool: True if the similarity is above the threshold, False otherwise.

---
**Raises**
- ValueError: If neither query nor formattedTag are provided.
- ValueError: If the OpenAI API key is not set in the config file.
