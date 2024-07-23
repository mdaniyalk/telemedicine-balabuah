"Module for conversion functions."
import os
from doc2docx import convert


def doc_to_docx_converter(doc_path):
    """
    Convert a .doc file to .docx format.

    Args:
        doc_path (str): The path to the .doc file.

    Returns:
        str: The path to the converted .docx file.
    """
    docx_path = doc_path.replace('.doc', '.docx')
    convert(doc_path, docx_path)
    os.remove(doc_path)  
    return docx_path
