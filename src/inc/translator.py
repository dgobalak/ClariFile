from googletrans import Translator as google_translator
from src.inc.lang_code_decipher import *


class Translator:
    def __init__(self, text, target):
        self.text = text
        self.target = target    # Can be code or full name
        self.translator = google_translator()

        self.translation = None
        self.lang_code = None
        
    def get_text_lang(self):
        if not self.lang_code:
            self.lang_code = self.translator.detect(self.text).lang

        return lang_code_to_name(self.lang_code)
    
    def translate(self):
        if not self.translation:
            self.translation = self.translator.translate(self.text, dest=self.target).text
        return self.translation
    