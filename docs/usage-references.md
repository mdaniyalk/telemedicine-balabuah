# References

## CLI Interface

The `app.py` script provides a command-line interface (CLI) for managing various tasks in the application. Below is the documentation for the available CLI commands and their respective options.

### Running the Flask Server

To start the Flask server:

```sh
python app.py run-server
```

This command reads the configuration from `config.toml` and runs the server using the specified `host` and `port`.

### Analyzing Folder Structure

To analyze the folder structure for the vectorstore:

```sh
python app.py analyze-folder-structure [OPTIONS]
```

> Options:
> 1. **`--db-path`**: Specifies the root path of the source documents. If not provided, it defaults to the `source_folder` value from `config.toml`.
>       - Example: `--db-path /path/to/source`
> 2. **`--output`**: Specifies the output path for the generated JSON file. If not provided, it defaults to the `json_folder_structure` value from `config.toml`.
>       - Example: `--output /path/to/output.json`

### Constructing the Vectorstore Database

To construct the vectorstore database:

```sh
python app.py construct-db [OPTIONS]
```

> Options:
> 1. **`--source_folder`**: Specifies the root path of the source documents. If not provided, it defaults to the `source_folder` value from `config.toml`.
>       - Example: `--source_folder /path/to/source`
> 2. **`--target_folder`**: Specifies the target destination path for the extracted vectorstore. If not provided, it defaults to the `target_folder` value from `config.toml`.
>       - Example: `--target_folder /path/to/vectorstore`
> 3. **`--json_path`**: Specifies the path to the JSON file containing the folder structure. If not provided, it defaults to the `json_folder_structure` value from `config.toml`.
>       - Example: `--json_path /path/to/folder-structure.json`




### Notes

- Ensure the `config.toml` file is correctly configured and located at the project root directory.
- Use the appropriate relative or absolute paths as required by the options.

### Error Handling

If an invalid command is provided, the script will print the help message and exit:

```sh
Invalid command
usage: app.py [-h] {run-server,analyze-folder-structure,construct-db} ...
```

Use the `-h` option with any command to get detailed help:

```sh
python app.py -h
```

### Example Usage

1. Starting the Server

    ```sh
    python app.py run-server
    ```

2. Analyzing Folder Structure with Custom Paths

    ```sh
    python app.py analyze-folder-structure --db-path /custom/source --output /custom/output.json
    ```

3. Constructing the Database with Default Paths

    ```sh
    python app.py construct-db
    ```

4. Constructing the Database with Custom Paths

    ```sh
    python app.py construct-db --source_folder /custom/source --target_folder /custom/target --json_path /custom/folder-structure.json
    ```


## API Reference

The Flask server in `app.py` provides several endpoints for managing chat sessions. Below is the detailed documentation for each API route.

The base URL for all endpoints is:
```
http://<your-server-address>/
```

1. Index

    `GET http://<your-server-address>/`

    Renders the chat interface. This can be used for interacting using the template web app.

    Returns

    ---
    Returns the HTML page `chat.html`.

---

2. Start Session

    `GET http://<your-server-address>/start-session`

    Initializes a new chat session.

    **Returns**

    ---    
    Returns a JSON object containing the `sessionId`.

    <!-- tabs:start -->

    #### **Example Request**

    ```bash
    curl -X GET "http://<your-server-address>/start-session"
    ```

    #### **Example Response**

    ```json
    {
        "sessionId": "<session_id>"
    }
    ```

    <!-- tabs:end -->

---

3. Chat

    `POST http://<your-server-address>/chat`

    Handles chat messages within a session. Sends a user message and receives a response from the chat session.

    **Request Body (Form or JSON)**
    
    ---
    `msg` *string* **Required**

    The user's message.

    ---
    `session_id` *string* **Required**

    The ID of the chat session.

    ---
    `response_type` *string* **Optional**

    Response type for the return. The default is `html`. Options are `html` and `json`

    **Returns**

    ---
    Returns the chat response (html snippet).

    <!-- tabs:start -->

    #### **Example Request**

    Form Body:

    ```bash
    curl -X POST http://<your-server-address>/chat \\
        -d "msg=Halo" \\
        -d "session_id=<session_id>" \\
        -d "response_type"="html"
    ```

    JSON Body:
    ```bash
    curl -X POST http://<your-server-address>/chat \\
        -H "Content-Type: application/json" \\
        -d '{"session_id": "<session_id>", "msg": "halo", "response_type": "json"}'
    ```

    #### **Example Response**

    HTML Response:
    ```html
    <p>Halo, apa yang bisa saya bantu?</p>
    ```

    JSON Response:
    ```json
    {
        "response": "Halo, apa yang bisa saya bantu?"
    }
    ```

    <!-- tabs:end -->

---

4. List Session

    `GET http://<your-server-address>/list-session`

    Lists chat sessions with pagination and ordering.

    **Request Query**

    ---
    `offset` *integer* **Optional**

    The starting point of the session list (default is 0).

    ---
    `per_page` *integer* **Optional**

    The number of sessions to return per page (default is 10).

    ---
    `order` *string* **Optional**

    The order of sessions, either `latest` or `oldest` (default is `latest`).

    **Returns**

    ---
    Returns a JSON object containing the list of sessions.

    <!-- tabs:start -->

    #### **Example Request**

    Without query params:
    ```bash
    curl -X GET http://<your-server-address>/list-session
    ```

    With query params:
    ```bash
    curl -X GET http://<your-server-address>/list-session?offset=0&per_page=10&order=latest
    ```

    #### **Example Response**

    ```json
    {
        "sessions": [
            {
                "session_id": "<session_id1>",
                "session_title": "example chat session 1",
                "timestamp": [
                    "Tue, 28 May 2024 14:49:53 GMT"
                ]
            },
            {
                "session_id": "<session_id2>",
                "session_title": "example chat session 2",
                "timestamp": [
                    "Tue, 28 May 2024 14:28:07 GMT"
                ]
            }
        ]
    }
    ```

    <!-- tabs:end -->

---

5. View Session

    `GET http://<your-server-address>/view-session`

    Retrieves detailed information about a specific chat session, including the conversation history.

    **Request Query**

    ---
    `session_id` *string* **Required**

    The ID of the chat session.

    **Returns**

    ---
    Returns a JSON object containing the session data.

    <!-- tabs:start -->

    #### **Example Request**

    ```bash
    curl -X GET http://<your-server-address>/view-session?session_id=<session_id>
    ```

    #### **Example Response**

    ```json
    {
        "session_id": "<session_id>",
        "session_title": "example chat session",
        "timestamp": [
            "Tue, 28 May 2024 14:28:07 GMT"
        ],
        "conversation": [
            {
                "message": "halo",
                "message_type": "user",
                "timestamp": "Tue, 28 May 2024 14:28:07 GMT"
            },
            {
                "message": "Apakah ada yang bisa saya bantu?",
                "message_type": "assistant",
                "timestamp": "Tue, 28 May 2024 14:28:25 GMT"
            }
        ]
    }
    ```

    <!-- tabs:end -->

---

6. Delete Session

    `POST http://<your-server-address>/delete-session`

    Deletes a specified chat session.

    **Request Body**

    ---
    `session_id` *string* **Required**
        
    The ID of the chat session to be deleted.
    
    **Returns**

    ---
    Returns a JSON object of success message.

    <!-- tabs:start -->

    #### **Example Request**

    ```bash
    curl -X POST http://<your-server-address>/delete-session \
        -H "Content-Type: application/json" \
        -d '{"session_id": "<session_id>"}'
    ```

    #### **Example Response**

    ```json
    {
        "message": "Session deleted."
    }
    ```

    <!-- tabs:end -->

---

7. Extract File

    `POST http://<your-server-address>/extract-file`

    Extracts a specified file.

    **Request Body**

    ---
    `file_path` *string* **Required**

    The path of the file to be extracted.

    ---
    `file_path_map` *string* **Required**

    The path map of the file to be extracted.

    ---
    `rel_file_path` *string* **Required**

    The relative file path for the extracted file.

    ---
    `additional_metadata` *object* **Optional**

    Additional metadata for the file extraction.

    ---
    `is_async` *boolean* **Optional** `Default: true`

    Whether the extraction should be asynchronous.

    **Returns**

    ---
    Returns a JSON object of success message.

    <!-- tabs:start -->

    #### **Example Request**

    ```bash
    curl -X POST http://<your-server-address>/extract-file \
        -H "Content-Type: application/json" \
        -d '{"file_path": "<file_path>", "file_path_map": "<file_path_map>", "rel_file_path": "<rel_file_path>", "additional_metadata": {}, "is_async": false}'
    ```

    #### **Example Response**

    ```json
    {
        "message": "<file_path> extracted successfully."
    }
    ```

    <!-- tabs:end -->

---

8. Extract Files

    `POST http://<your-server-address>/extract-files`

    Extracts multiple files.

    **Request Body**

    ---
    `file_paths` *array* **Required**

    The paths of the files to be extracted.

    ---
    `file_path_maps` *array* **Required**

    The path maps of the files to be extracted.

    ---
    `rel_file_paths` *array* **Required**

    The relative file paths for the extracted files.

    ---
    `additional_metadatas` *array* **Optional**

    Additional metadata for the file extractions.

    ---
    `is_async` *boolean* **Optional** `Default: true`

    Whether the extractions should be asynchronous.

    **Returns**

    ---
    Returns a JSON object of success message.

    <!-- tabs:start -->

    #### **Example Request**

    ```bash
    curl -X POST http://<your-server-address>/extract-files \
        -H "Content-Type: application/json" \
        -d '{"file_paths": ["<file_path1>", "<file_path2>"], "file_path_maps": ["<file_path_map1>", "<file_path_map2>"], "rel_file_paths": ["<rel_file_path1>", "<rel_file_path2>"], "additional_metadatas": [{}], "is_async": false}'
    ```

    #### **Example Response**

    ```json
    {
        "message": "[<file_path1>, <file_path2>] extracted successfully."
    }
    ```

    <!-- tabs:end -->

---

9. Delete File

    `POST http://<your-server-address>/delete-file`

    Deletes a specified file.

    **Request Body**

    ---
    `file_path` *string* **Required**

    The path of the file to be deleted.

    ---
    `file_path_map` *string* **Required**

    The path map of the file to be deleted.

    ---
    `rel_file_path` *string* **Required**

    The relative file path for the file to be deleted.

    **Returns**

    ---
    Returns a JSON object of success message.

    <!-- tabs:start -->



    #### **Example Request**

    ```bash
    curl -X POST http://<your-server-address>/delete-file \
        -H "Content-Type: application/json" \
        -d '{"file_path": "<file_path>", "file_path_map": "<file_path_map>", "rel_file_path": "<rel_file_path>"}'
    ```

    #### **Example Response**

    ```json
    {
        "message": "<file_path> deleted successfully."
    }
    ```

    <!-- tabs:end -->

---

10. Delete Files

    `POST http://<your-server-address>/delete-files`

    Deletes multiple files.

    **Request Body**

    ---
    `file_paths` *array* **Required**

    The paths of the files to be deleted.

    ---
    `file_path_maps` *array* **Required**

    The path maps of the files to be deleted.

    ---
    `rel_file_paths` *array* **Required**

    The relative file paths for the files to be deleted.

    **Returns**

    ---
    Returns a JSON object of success message.

    <!-- tabs:start -->

    #### **Example Request**

    ```bash
    curl -X POST http://<your-server-address>/delete-files \
        -H "Content-Type: application/json" \
        -d '{"file_paths": ["<file_path1>", "<file_path2>"], "file_path_maps": ["<file_path_map1>", "<file_path_map2>"], "rel_file_paths": ["<rel_file_path1>", "<rel_file_path2>"]}'
    ```

    #### **Example Response**

    ```json
    {
        "message": "[<file_path1>, <file_path2>] deleted successfully."
    }
    ```

    <!-- tabs:end -->

---

## Error Handling

### Common HTTP Status Codes

- `200 OK`: The request has succeeded.
- `400 Bad Request`: The request could not be understood by the server due to malformed syntax.
- `404 Not Found`: The requested resource could not be found.
- `500 Internal Server Error`: The server encountered an unexpected condition which prevented it from fulfilling the request.

### Example Error Response

```json
{
    "error": "An error message explaining what went wrong."
}
```

This concludes the documentation for the Flask server endpoints. If you need further assistance or have additional questions, please let me know!