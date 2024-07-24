from telemedicine.core.base import openai_chat
from telemedicine.core.translate import translate

def paraphrase(text, text_type='error-msg'):
    """
    This function takes a text as input and returns the paraphrased text.
    """
    if text_type == 'error-msg':
        prompt = f"""
        Paraphrase the following error text to make the user more understand the context, 
        you can also suggest the user how to handle the error. Paraphrase and suggest in beautiful markdown format using Bahasa Indonesia.
        Anwers this in very simple language and easy to understand. Don't include word like 'Paraphrase'.
        Error message: '{text}'"""
    else:
        raise ValueError(f"Invalid text type: {text_type}")
    paraphrased_text = openai_chat(
        question=prompt,
        model="llama3-8b-8192",
        )
    paraphrased_text = translate(paraphrased_text, from_lang='auto', to_lang='id')
    
    return paraphrased_text