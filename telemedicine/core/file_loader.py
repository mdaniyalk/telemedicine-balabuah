"Module for loading various types of documents."
import os
import mammoth
import markdownify
import tempfile

from langchain_community.document_loaders.pdf import PyPDFLoader, UnstructuredPDFLoader
from langchain_community.document_loaders.markdown import UnstructuredMarkdownLoader
from langchain_community.document_loaders.word_document import UnstructuredWordDocumentLoader
from langchain_community.document_loaders.unstructured import UnstructuredFileLoader
from langchain_community.document_loaders.excel import UnstructuredExcelLoader


from telemedicine.core.converter import doc_to_docx_converter


def file_loader(path):
    """
    Load a document from the specified path.

    Args:
        path (str): The path to the document file.

    Returns:
        The loaded document data.
    """
    _doc = []
    if '.pdf' in path:
        _doc = pdf_loader(path)
    elif '.doc' in path:
        if '.docx' not in path:
            path = doc_to_docx_converter(path)
        _doc = docx_loader(path)
    elif '.xlsx' in path:
        _doc = UnstructuredExcelLoader(path).load()
    else:
        if '.DS_Store' not in path:
            _doc = UnstructuredFileLoader(path).load()
    return _doc


def docx_loader(doc_path):
    """
    Load a .docx document.

    Args:
        doc_path (str): The path to the .docx document file.

    Returns:
        The loaded document data.
    """
    with open(doc_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
    html = result.value
    markdown = markdownify.markdownify(html)
    temp_md_file = tempfile.NamedTemporaryFile(delete=False, suffix=".md")
    temp_md_path = temp_md_file.name
    try:
        with open(temp_md_path, "w") as md_file:
            md_file.write(markdown)
        
        # Load the data from the markdown file
        data = UnstructuredMarkdownLoader(temp_md_path, metadata_filename=doc_path).load()
        for d in data:
            d.metadata['source'] = doc_path
        os.remove(temp_md_path)
    except Exception as e:
        print(f'Warning, an error occurred: {e}. Falling back to loading with UnstructuredWordDocumentLoader.')
        try:
            data = UnstructuredWordDocumentLoader(doc_path).load()
        except Exception as e:
            print(f"An error occurred: {e}. The document could not be loaded.")
            raise Exception("The DOCX document could not be loaded." ) from e
    return data


def pdf_loader(pdf_path):
    try:
        data = PyPDFLoader(pdf_path, extract_images=True).load()
    except Exception as e:
        print(f"Warning, an error occurred: {e}. Falling back to loading without images.")
        try:
            data = PyPDFLoader(pdf_path, extract_images=False).load()
        except Exception as e:
            print(f"Warning, an error occurred: {e}. Falling back to unstructured loading.")
            try:
                data = UnstructuredPDFLoader(pdf_path).load()
            except Exception as e:
                print(f"An error occurred: {e}. The PDF document could not be loaded.")
                raise Exception("The PDF document could not be loaded." ) from e
    return data

