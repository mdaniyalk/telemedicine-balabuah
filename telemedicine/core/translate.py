"Module for translation functionality."
from deep_translator import GoogleTranslator
from langdetect import detect

def translate(text, from_lang, to_lang):
    """
    Translate text from one language to another.

    Args:
        text (str): The text to be translated.
        from_lang (str): The language of the original text.
        to_lang (str): The language to translate the text into.

    Returns:
        str: The translated text.
    """
    if from_lang == 'auto':
        from_lang = detect(text[:4500])
        if from_lang == to_lang:
            return text
    if len(text) > 4800:
        return text
    translator = GoogleTranslator(source=from_lang, target=to_lang)
    translated_text = translator.translate(text)
    return translated_text
