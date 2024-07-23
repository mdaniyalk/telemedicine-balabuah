# Example Usage

## CLI Interface

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