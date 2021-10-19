from nltk import pos_tag, ne_chunk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tree import Tree
from nltk import FreqDist
import itertools


class TopicSelector:
    def __init__(self, text, min_freq=3, lang="english"):
        self.text = text
        self.min_freq = min_freq
        self.lang = lang

        self.named_entities = None
        self.common_words = None
        self.prop_nouns = None
        self.keywords = None
    
    def get_keywords(self):
        return self.keywords if self.keywords else self._set_keywords()

    def get_named_entities(self):
        return self.named_entities if self.named_entities else self._set_named_entities()

    def get_common_words(self):
        return self.common_words if self.common_words else self._set_common_words()

    def get_prop_nouns(self):
        return self.prop_nouns if self.prop_nouns else self._set_prop_nouns()

    def _set_keywords(self):
        ne = set(self.get_named_entities())
        cw = set(self.get_common_words())
        pn = set(self.get_prop_nouns())
        self.keywords = set(itertools.chain(ne, cw, pn))
        return self.keywords

    def _get_stopwords(self):
        return set(stopwords.words("english"))

    def _filter_stopwords(self, text):
        words = word_tokenize(text, language=self.lang)
        stopwords = self._get_stopwords()
        filtered_words = [word for word in words if word.casefold() not in stopwords]
        return filtered_words
    
    def _lemmatize_words(self, text):
        lemmatizer = WordNetLemmatizer()
        filtered_words = self._filter_stopwords(text)
        lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]
        return lemmatized_words

    def _tag_words(self, text):
        tagged_words = pos_tag(self._lemmatize_words(text))
        return tagged_words

    def _set_named_entities(self):
        tagged_words = self._tag_words(self.text)
        tree = ne_chunk(tagged_words, binary=True)
        named_entities = []
        current_chunk = []

        for i in tree:
            if type(i) == Tree:           
                current_chunk.append(" ".join([token for token, pos in i.leaves()]))
                if current_chunk:
                    named_entity = " ".join(current_chunk)                  
                    if named_entity not in named_entities:
                        named_entities.append(named_entity)
                        current_chunk = []
            else:
                continue

        self.named_entities = named_entities
        return self.named_entities

    def _set_common_words(self):
        freq_dist = FreqDist(self._lemmatize_words(self.text))
        self.common_words = [x[0] for x in freq_dist.most_common(20) if x[1] >= self.min_freq]
        return self.common_words

    def _set_prop_nouns(self):
        tagged_words = self._tag_words(self.text)
        self.prop_nouns = [x[0] for x in tagged_words if x[1] == "NNP"]
        return self.prop_nouns