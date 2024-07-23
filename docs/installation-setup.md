# Installation & Configuration

We recommend to install this on a separated python environment. For this, we use conda environment.

## Installing python (Conda) Environment

1. Download and install Anaconda from https://www.anaconda.com/products/distribution

2. Configuring Environment
    - **Using Makefiles**

        Natively, Makefiles are supported on linux and macOS, to use on Windows, see https://earthly.dev/blog/makefiles-on-windows/ 
        
        1. Create a new environment
            ```bash
            make create-env 
            ```
            Note: the default environment name is "rag". 
            To change env name from 'rag' to others, edit conda.yml and Makefile

        2. Activate the environment
            ```bash
            make activate-env
            ```
            To change env name from 'rag' to others, edit conda.yml and Makefile

        3. Install the package
            ```bash
            make install
            ```

    - **Manual Configuration**
        1. Create a new environment
            ```bash
            conda env create -f environments/conda.yml
            ```
            Note: the default environment name is "rag". 
            To change env name from 'rag' to others, edit conda.yml and Makefile

        2. Activate the environment
            ```bash
            conda activate rag
            ```
            To change env name from 'rag' to others, edit conda.yml and Makefile

        3. Install the package
            ```bash
            pip install -r environments/requirements.txt
            ```

    For other virtual environment, you can use similar approach to anaconda

## Configuring App
To configure the application, you need to create and edit the `example-config.toml` file at the project root directory and save as `config.toml` at the same root directory. The configuration includes the following sections:

```toml
# example-config.toml

[server_config]
host = "0.0.0.0"
port = 8000


[openai_config]
openai_key = "api-key"
openai_base_url = "https://api.openai.com/v1"
openai_organization = "example_organization"
openai_proxy = "http://proxy.example.com"
openai_main_model = "gpt-4-0125-preview"
openai_secondary_model = "gpt-3.5-turbo-0125"
openai_tertiary_model = "gpt-4o-2024-05-13"
openai_default_chat_system_message = "You are a helpful assistant that help employee understand company documents."
openai_embedding_model = "text-embedding-3-small"
openai_retry_max = 5
openai_retry_multiplier = 0.5
openai_retry_stop = 3


[db_config]
source_folder = "example-sources"
target_folder = "example-vectorstore"
json_folder_structure = "example-folder-structure.json"
use_relative_paths = true

folder_names = ["nama_alat", "nama_prosedur"]

folder_name_definitions = { "nama_alat" = "Nama Alat", "nama_prosedur" = "Nama Prosedur" }

example_data = { "nama_alat" = "alat1, alat2, etc.", "nama_prosedur" = "prosedur-a, prosedur-b, etc." }

```

1. **[server_config]**
    
    This config defines the server settings for hosting the web application.
    1. **host**: **Required** 
        
        The IP address used for serving the web application.
        - Default: `"0.0.0.0"`
    2. **port**: **Required** 
    
        The port number used for serving the web application.
        - Default: `8000`

2. **[openai_config]**

    This config contains the configuration for interacting with the OpenAI API.
    1. **openai_key**: **Required** 

        The API key provided by OpenAI.
    2. **openai_base_url**: **Optional** 
        
        The base URL endpoint for the OpenAI API.
        - Default: `"https://api.openai.com/v1"`
    3. **openai_organization**: **Optional** 
    
        The organization ID found in the Account Organization settings page.
        - Default: `None`
    4. **openai_proxy**: **Optional** 
    
        The proxy server's address if the network environment requires it to access external services.
        - Default: `None`
    5. **openai_main_model**: **Required** 
    
        The primary model used for OpenAI API interactions. This will be used for most of the LLM content generation.
        - Default: `"gpt-3.5-turbo-0125"`
        - Example: `"gpt-4-0125-preview"`
    6. **openai_secondary_model**: **Required** 
    
        A secondary model option for OpenAI API interactions. This will be used for the less important task such as summarization, etc.
        - Default: `"gpt-3.5-turbo-0125"`
        - Example: `"gpt-3.5-turbo-0125"`
    7. **openai_tertiary_model**: **Required** 
    
        An additional model option for OpenAI API interactions. This will be used for the final prompt output.
        - Default: `"gpt-3.5-turbo-0125"`
        - Example: `"gpt-4o-2024-05-13"`
    8. **openai_default_chat_system_message**: **Optional** 
    
        The default system message for chat interactions.
        - Default: `"You are a helpful assistant."`
        - Example: `"You are a helpful assistant that helps employees understand company documents."`
    9. **openai_embedding_model**: **Required** 
    
        The model used for generating text embeddings. Make sure that the generated vectorstore and the current session use the same embedding model.
        - Default: `"text-embedding-3-small"`
        - Example: `"text-embedding-3-small"`
    10. **openai_retry_max**: **Optional** 
    
        The maximum number of retries for API requests.
        - Default: `5`
    11. **openai_retry_multiplier**: **Optional** 
    
        The multiplier for exponential backoff during retries.
        - Default: `0.5`
    12. **openai_retry_stop**: **Optional** 
    
        The stop condition for retry attempts.
        - Default: `3`

3. **[db_config]**

    This configuration configures the database for storing and organizing the document vectors.
    1. **source_folder**: **Required** 
    
        The folder path for source documents used in the retrieval. Use a relative path corresponding to the root path.
        - Example: `"example-sources"`
    2. **target_folder**: **Required** 
    
        The destination folder for the generated vector database. Use a relative path corresponding to the root path.
        - Example: `"example-vectorstore"`
    3. **json_folder_structure**: **Required** 
    
        The JSON file defining the folder structure that will be generated later.
        - Example: `"example-folder-structure.json"`
    4. **use_relative_paths**: **Required** 
    
        Specifies whether to use relative paths.
        - Example: `true`
        - Options: `[true, false]`
    5. **folder_names**: **Required** 
    
        A list of folder names that define the structure of the document database.
        - Example: `["nama_alat", "nama_prosedur"]`
    6. **folder_name_definitions**: **Required** 
    
        A dictionary mapping folder name keys to their definitions.
        - Example: `{ "nama_alat" = "Nama Alat", "nama_prosedur" = "Nama Prosedur" }`
    7. **example_data**: **Optional**  
    
        Example data definitions for folder names.
        - Example: `{ "nama_alat" = "alat1, alat2, etc.", "nama_prosedur" = "prosedur-a, prosedur-b, etc." }`

Ensure the folder structure for the source documents and the target vector database follows the specified configurations. This allows the application to correctly read and store the documents for retrieval purposes.