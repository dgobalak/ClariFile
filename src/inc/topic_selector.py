from src.inc.lang_detection_utils import *
from nltk import pos_tag, ne_chunk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tree import Tree
from nltk import FreqDist
import itertools


class TopicSelector:
    def __init__(self, text: str, min_freq: int = 3, lang: str = "auto", n_common_words: int = 20) -> None:
        self.text = text
        self.min_freq = min_freq
        self.n_common_words = n_common_words
        self.lang = detect_lang(self.text) if lang == 'auto' else lang

        self.named_entities = None
        self.common_words = None
        self.keywords = None

    def get_keywords(self) -> set:
        return self.keywords if self.keywords else self._set_keywords()

    def get_named_entities(self) -> list:
        return self.named_entities if self.named_entities else self._set_named_entities()

    def get_common_words(self) -> list:
        return self.common_words if self.common_words else self._set_common_words()

    def _set_keywords(self) -> set:
        self.keywords = set(self.get_named_entities())
        return self.keywords

    def _get_stopwords(self) -> set:
        return set(stopwords.words("english"))

    def _filter_stopwords(self, text: str) -> list:
        words = word_tokenize(text, language=self.lang)
        stopwords = self._get_stopwords()
        filtered_words = [
            word for word in words if word.casefold() not in stopwords]
        return filtered_words

    def _lemmatize_words(self, text: str) -> list:
        lemmatizer = WordNetLemmatizer()
        filtered_words = self._filter_stopwords(text)
        lemmatized_words = [lemmatizer.lemmatize(
            word) for word in filtered_words]
        return lemmatized_words

    def _tag_words(self, text: str) -> list:
        tagged_words = pos_tag(self._lemmatize_words(text))
        return tagged_words

    def _set_named_entities(self) -> list:
        tagged_words = self._tag_words(self.text)
        tree = ne_chunk(tagged_words, binary=True)
        named_entities = []
        current_chunk = []

        for i in tree:
            if type(i) == Tree:
                current_chunk.append(
                    " ".join([token for token, pos in i.leaves()]))
                if current_chunk:
                    named_entity = " ".join(current_chunk)
                    if named_entity not in named_entities:
                        named_entities.append(named_entity)
                        current_chunk = []
            else:
                continue

        self.named_entities = named_entities
        return self.named_entities

    # No longer used in keyword extraction for summarization
    # Will be used for definitions
    def _set_common_words(self) -> list:
        freq_dist = FreqDist(self._lemmatize_words(self.text))
        self.common_words = [x[0] for x in freq_dist.most_common(
            self.n_common_words) if x[1] >= self.min_freq and len(x[0]) > 1]
        return self.common_words
