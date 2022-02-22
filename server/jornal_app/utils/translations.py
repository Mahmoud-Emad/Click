from googletrans import Translator

def translate_method(text, code="en"):
    """Utils function to translate text using google translation api"""
    translator = Translator()
    text_ = translator.translate(text, dest=code)
    return text_.text