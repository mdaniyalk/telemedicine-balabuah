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

    Rules:
    1. If the question is a simple statement or greeting (e.g., hi, hai, hello, halo), you may respond directly without referring to the context.
    2. If the question does not pertain to health, mental health, nutrition, or any other medical/health-related topic, don't answers that question. Force the user to ask a health-related question instead.
    3. Keep in mind that by default, you're a health related assistant, so please just answers the question related to that.
    
    Context:
    {context}

    Question: {question}
    
    
    You need to make sure that your answers are relevant and accurate. 
    If there is a table, please response in markdown table or using bullet points or anything that are readable.

    Answer in Bahasa Indonesia using beautiful markdown format:"""

    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    return prompt


def multi_query_retriver_prompt():
    """
    Generate a prompt for multi-query retrieval.

    Returns:
        PromptTemplate: The prompt template for multi-query retrieval.
    """
    prompt_template = """
    You are an AI Assistant who helps people to find information about health.
    Now, your task is to generate 2 different versions of the given user 
    question to retrieve relevant documents from a vector database. 
    By generating multiple perspectives on the user question, 
    your goal is to help the user overcome some of the limitations 
    of distance-based similarity search. Provide these alternative 
    questions separated by newlines. You can use the given document summary to generate the questions.
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

def get_help_template():
    name = "Bu Bidan Novi Marissa"
    number = "0852-7270-4070"
    number_link = "https://wa.me/6285272704070"
    prompt_list = [
        f"Jika anda memerlukan bantuan kesehatan lebih lanjut, silahkan hubungi `{name}` di Whatsapp [{number}]({number_link}).",
        f"Jika Anda membutuhkan dukungan kesehatan lebih lanjut, jangan ragu untuk menghubungi `{name}` di Whatsapp pada [{number}]({number_link}).",
        f"Hubungi `{name}` di Whatsapp di [{number}]({number_link}) jika Anda membutuhkan bantuan kesehatan lebih lanjut.",
        f"Untuk informasi kesehatan lebih lanjut, silakan menghubungi `{name}` di Whatsapp di [{number}]({number_link}).",
        f"Jika Anda memerlukan bantuan tambahan mengenai kesehatan, silakan hubungi `{name}` melalui Whatsapp di [{number}]({number_link}).",
        f"Untuk mendapatkan bantuan kesehatan lebih lanjut, hubungi `{name}` di Whatsapp di [{number}]({number_link}).",
        f"Untuk bantuan lebih lanjut mengenai kesehatan, silakan menghubungi `{name}` melalui Whatsapp di [{number}]({number_link}).",
        f"Bila Anda membutuhkan informasi lebih lengkap mengenai kesehatan atau memerlukan bantuan tambahan, silakan hubungi `{name}` melalui Whatsapp di [{number}]({number_link}). ",
    ]

    return random.choice(prompt_list)