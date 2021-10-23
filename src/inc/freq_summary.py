from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import re
import heapq


class MostFrequentSummary:
    def __init__(self, text, max_sent_len=30, summary_len=8, lang="english"):
        self.text = self._preprocess(text)
        self.max_sent_len = max_sent_len
        self.summary_len = summary_len
        self.lang = lang

        self.formatted_text = self._format_text(self.text)
        self.summary = None

    def get_summary(self):
        return self.summary if self.summary else self._summarize()

    def _summarize(self):
        word_freqs = self._calculate_word_freqs(self.formatted_text)
        sent_freqs = self._calculate_sent_freqs(self.text, word_freqs)
        summary_sentences = heapq.nlargest(self.summary_len, sent_freqs, key=sent_freqs.get)
        self.summary = ' '.join(summary_sentences)
        return self.summary

    def _preprocess(self, t):
        text = re.sub(r'\[[0-9]*\]', ' ', t)
        text = re.sub(r'\s+', ' ', text)
        return text

    def _format_text(self, t):
        formatted_text = re.sub('[^a-zA-Z]', ' ', t)
        formatted_text = re.sub(r'\s+', ' ', formatted_text)
        return formatted_text
    
    def _tokenize_sentences(self, text):
        return sent_tokenize(text)

    def _get_stopwords(self):
        return set(stopwords.words("english"))

    def _filter_stopwords(self, text):
        words = word_tokenize(text, language=self.lang)
        stopwords = self._get_stopwords()
        filtered_words = [word for word in words if word.casefold() not in stopwords]
        return filtered_words

    def _calculate_word_freqs(self, f_text):
        word_freqs = {}
        for word in self._filter_stopwords(f_text):
            if word not in word_freqs.keys():
                word_freqs[word] = 1
            else:
                word_freqs[word] += 1

        word_freqs = self._normalize_freqs(word_freqs)
        return word_freqs

    def _normalize_freqs(self, word_freqs):
        max_freq = max(word_freqs.values())
        for word in word_freqs.keys():
            word_freqs[word] = (word_freqs[word]/max_freq)
        return word_freqs

    def _calculate_sent_freqs(self, text, word_freqs):        
        sentence_scores = {}
        for sentence in self._tokenize_sentences(self.text):
            for word in word_tokenize(sentence.lower()):
                if word in word_freqs.keys():
                    if len(sentence.split(' ')) < self.max_sent_len:
                        if sentence not in sentence_scores.keys():
                            sentence_scores[sentence] = word_freqs[word]
                        else:
                            sentence_scores[sentence] += word_freqs[word]
        return sentence_scores
