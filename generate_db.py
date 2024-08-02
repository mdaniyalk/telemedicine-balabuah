import argparse

from telemedicine.core.vectorstore import VectorDB
parser = argparse.ArgumentParser(description="Load documents from files into the vector store.")
parser.add_argument("--folder_path", type=str, help="The path to the folder containing the documents.")
args = parser.parse_args()

vectorstore = VectorDB(
    model_name="",
    embedding_model="BAAI/bge-small-en-v1.5" 
)
vectorstore.load_document_from_folder(args.folder_path)