from nltk import pos_tag, ne_chunk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tree import Tree
from nltk import FreqDist

class TopicSelector:
    def __init__(self, text, min_freq=3, lang="english"):
        self.text = text
        self.min_freq = min_freq
        self.lang = lang
        self._stopwords = self._get_stopwords()

        self.lemmatized_words = None
        self.tagged_words = None
        self.named_entities = None
        self.common_words = None
        self.prop_nouns = None
        self.keywords = None
        self._lemmatize_words()
    
    def get_keywords(self):
        if not self.keywords:
            self._set_keywords()
        return self.keywords

    def get_named_entities(self):
        if not self.named_entities:
            self._set_named_entities()
        return self.named_entities

    def get_common_words(self):
        if not self.common_words:
            self._set_common_words()
        return self.common_words

    def get_prop_nouns(self):
        if not self.prop_nouns:
            self._set_prop_nouns()
        return self.prop_nouns

    def _set_keywords(self):
        ne = set(self.get_named_entities())
        cw = set(self.get_common_words())
        pn = set(self.get_prop_nouns())
        self.keywords = ne.symmetric_difference(cw).symmetric_difference(pn)

    def _get_stopwords(self):
        return set(stopwords.words("english"))

    def _filter_stopwords(self):
        words = word_tokenize(self.text, language=self.lang)
        filtered_words = [word for word in words if word.casefold() not in self._stopwords]
        return filtered_words
    
    def _lemmatize_words(self):
        lemmatizer = WordNetLemmatizer()
        filtered_words = self._filter_stopwords()
        self.lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]

    def _set_named_entities(self):
        self.tagged_words = pos_tag(self.lemmatized_words)
        tree = ne_chunk(self.tagged_words, binary=True)
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

    def _set_common_words(self):
        freq_dist = FreqDist(self.lemmatized_words)
        self.common_words = [x[0] for x in freq_dist.most_common(20) if x[1] >= self.min_freq]

    def _set_prop_nouns(self):
        if not self.tagged_words:
            self.tagged_words = pos_tag(self.lemmatized_words)

        self.prop_nouns = [x[0] for x in self.tagged_words if x[1] == "NNP"]