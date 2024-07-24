"""
Module for defining prompts for retrieval question answering and multi-query retrieval.
"""
import random

from langchain.prompts import PromptTemplate


def retrieval_qa_prompt():
    """
    Generate a prompt for retrieval question answering based on the given history.

    Args:
        history (str): The chat history.

    Returns:
        PromptTemplate: The prompt template for retrieval question answering.
    """
    prompt_template = """
    Given the context below, answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    
    Context:
    {context}

    Question: {question}
    
    
    You need to make sure that your answers are relevant and accurate. 
    If the answers is a procedure or instruction, you should make the answers as clear as possible, 
    with the correct order. Make sure that you didn't combine combine multiple procedures from 
    different tools or tool parts, as many tools have similar types of procedures.
    Make sure you didn't add any information that is not in the context.
    Please make sure that the answers is correct, since my boss will fire me if you mess up.
    If the context provided didn't help you to answer the question, 
    you can ask for more information or just say that you don't know the answer.
    If the question is just a statement or a greeting, you can answer that 
    question according to your knowledge without using the context.
    If there is a table, please response in markdown table or using bullet points or anything that are readable.
    At the end, you need to also give references and suggest user to check to this list of documents:
    {doc_references}

    Answer in Bahasa Indonesia using beautiful markdown format:"""

    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    return prompt


def multi_query_retriver_prompt(document_summary):
    """
    Generate a prompt for multi-query retrieval.

    Returns:
        PromptTemplate: The prompt template for multi-query retrieval.
    """
    prompt_template = f"""
    You are an AI Assistant who helps employees understand questions about company procedures. 
    Most of the document are report, working instruction, manual guide, and other company procedures.
    Now, your task is to generate 2 different versions of the given user 
    question to retrieve relevant documents from a vector database. 
    By generating multiple perspectives on the user question, 
    your goal is to help the user overcome some of the limitations 
    of distance-based similarity search. Provide these alternative 
    questions separated by newlines. You can use the given document summary to generate the questions.
    Document Summary:
    {document_summary}
    """
    prompt_template += """
    Original question: {question}"""

    prompt = PromptTemplate(input_variables=["question"], template=prompt_template)

    return prompt


def standalone_question_from_history(question, history):
    prompt = f"""
    Given the following conversation between a user and an AI assistant and a follow up question from user, rephrase the follow up question to be a standalone question. 
    If possible, ensure that the standalone question summarizes the main point of the conversation 
    and completes the follow up question with all the necessary context from the history.
    If the follow up question is differ from history, just rephrase the follow up question to be a standalone question.
    Chat History:
    {history}
    Follow Up Input: {question}
    Standalone question:
    """
    return prompt
