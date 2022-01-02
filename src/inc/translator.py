from googletrans import Translator as google_translator
from src.inc.lang_detection_utils import *


class Translator:
    def __init__(self, text: str, target: str) -> None:
        self.text = text
        self.target = target    # Can be code or full name
        self.translator = google_translator()

        self.lang = detect_lang(self.text)
        self.translation = None

    def get_text_lang(self) -> str:
        if not self.lang:
            self.lang = detect_lang(self.text)

        return self.lang

    def translate(self) -> str:
        if not self.translation:
            self.translation = self.translator.translate(
                self.text, dest=self.target, src=self.lang).text
        return self.translation
