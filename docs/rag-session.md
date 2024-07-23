# telemedicine.session
Module that handle the user session and history

---

## ChatSession
```python
class telemedicine.session.ChatSession()
```
Class representing a chat session.


---
**Attributes:**

- **session_id**: `str`

    The unique session ID of the user.
- **chat_session**: [`Chat`](rag-chat?id=chat)

    Chat instances of the current session.
- **filename**: `str`

    Session ID save directory

---
**Methods**

```python
load(session_id)
```
Load a chat session.

Parameters:
- session_id (str)

    The session ID.

---
```python
load_from_file(filename)
```
Load a chat session from a file.

Parameters:
- filename (str)

    The name of the file to load the session from.

---
```python
delete_session()
```
Delete the current chat session file.

---
```python
initialize(session_id)
```
Initialize a new chat session.

---
```python
save_session(session_id)
```
Save the chat session.

---
```python
copy_chat(session_id)
```
Copy the chat session.

Returns:
- [Chat](rag-chat?id=chat): The copied chat session.

---
```python
_initialize_session(session_id)
```
Wrapper method for `initialize(session_id)`.

Returns:
- str: The session ID.

---
```python
get_response(msg, html=True)
```
Get the response to a given message.

Parameters:
- msg (str)

    The message to get a response for.

- html (bool, optional)
    
    Whether to format the response as HTML. Defaults to False.

Returns:
- str: The response to the message.

---
```python
get_dict(with_conversation=False)
```
Get a dictionary representation of the chat session.

Parameters:
- with_conversation (bool, optional)

    Whether to include the conversation history. Defaults to False.

Returns:
- Dict[str, Any]: A dictionary containing the session data.

---
**Class Methods**

```python
ChatSession.get_session_data(session_filename=None, session_id=None, with_conversation=None)
```
Retrieve the result for a given question.

Parameters:
- qsession_filename (str, optional)

    The filename of the session data file. Defaults to None.

- session_id (str, optional)
    
    The session ID. Defaults to None.

- with_conversation (bool, optional)
    
    Whether to include the conversation history. Defaults to False.

Returns:
- Dict[str, Any]: A dictionary containing the session data.

Raises:
- ValueError: If neither session_filename nor session_id is provided.

---
