from nltk.tokenize import sent_tokenize 
from nltk.corpus import stopwords
from nltk.cluster import KMeansClusterer, euclidean_distance, cosine_distance
from gensim.models import Word2Vec
from scipy.spatial import distance
import re


class ClusterSummary:
    def __init__(self, text, min_word_freq=1, dist_metric="euclidean", n_clusters=8, lang="english"):
        self.text = self._preprocessing(text)
        self.min_word_freq = min_word_freq
        self.dist_metric = self._set_distance_metric(dist_metric)

        self.n_clusters = n_clusters
        self.lang = lang

        self.summary = None

    def get_summary(self):
        return self.summary if self.summary else self._create_summary()

    def _create_summary(self):
        sentences = self._get_sentences(self.text)
        cleaned_sentences = self._clean_sentences(sentences)
        all_words = self._words_from_sentence_list(cleaned_sentences)

        w2v_model = self._get_w2v_model(all_words)
        sent_vector = self._vectorize_sentences(cleaned_sentences, w2v_model)
        kclusterer = self._create_clusterer(len(sent_vector))
        clusters = self._get_sent_clusters(kclusterer, sent_vector)
        centroids = self._get_cluster_centroids(kclusterer)
        
        summary_indices = [] 
        for cluster_index in range(self.n_clusters):
            distances = {}
            for j in range(len(clusters)):
                if clusters[j] == cluster_index:
                    distances[j] = distance.euclidean(centroids[cluster_index], sent_vector[j])

            summary_indices.append(min(distances, key=distances.get))

        summary = []
        for i in summary_indices:
            summary.append(sentences[i])
        summary = " ".join(summary)

        return summary

    def _set_distance_metric(self, dist):
        if dist == "cosine":
            return cosine_distance
        elif dist == "euclidean":
            return euclidean_distance

    def _get_sentences(self, text):
        return sent_tokenize(text)

    def _preprocessing(self, t):
        text = t[2:-1].replace("\\r\\n", " ")
        text = text.replace("\\n", " ")
        text = text.replace("\\x0c", " ")
        text = ' '.join(text.split()).strip()

        text = re.sub(r'\[[0-9]*\]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text

    def _clean_sentences(self, sentences):
        cleaned_txt = []
        for i in range(len(sentences)):
            sen = re.sub('[^a-zA-Z]', " ", sentences[i])  
            sen = sen.lower()                            
            sen = sen.split()                         
            sen = ' '.join([i for i in sen if i not in stopwords.words(self.lang)])   
            cleaned_txt.append(sen)
        return cleaned_txt

    def _words_from_sentence_list(self, sentences):
        return [sentence.split() for sentence in sentences]

    def _get_w2v_model(self, all_words):
        return Word2Vec(all_words, min_count=self.min_word_freq)

    def _vectorize_sentences(self, cleaned_sentences, model):
        sent_vector=[]
        for sentence in cleaned_sentences:
            plus=0
            for j in sentence.split():
                plus += model.wv[j]

            # TODO: Deal with situation when len(sentence.split()) == 0
            plus = plus/len(sentence.split())
            sent_vector.append(plus)
            
        return sent_vector

    def _create_clusterer(self, num_sentences):
        # Limit n_clusters so it doesn't exceed the number of sentences in the text
        self.n_clusters = self.n_clusters if self.n_clusters <= num_sentences else num_sentences
        return KMeansClusterer(num_means=self.n_clusters, distance=self.dist_metric)

    def _get_sent_clusters(self, kclusterer, sentence_vectors):
        clusters = kclusterer.cluster(sentence_vectors, True)
        return clusters

    def _get_cluster_centroids(self, kclusterer):
        means = kclusterer.means()
        return means
