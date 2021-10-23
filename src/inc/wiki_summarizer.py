from src.inc.freq_summary import MostFrequentSummary
from src.inc.cluster_summary import ClusterSummary
from urllib.error import HTTPError
import urllib.request
import bs4 as bs


class WikiSummarizer():
    def __init__(self, keywords, summarizer="freq", min_word_freq=1, dist_metric="cosine", n_clusters=8, max_sent_len=30, summary_len=8, lang='english', min_summary_char_len=100):
        self.keywords = keywords
        self.lang = lang
        self.summarizer = summarizer

        # Cluster summary config
        self.min_word_freq = min_word_freq
        self.dist_metric = dist_metric
        self.n_clusters = n_clusters

        # Frequency summary config
        self.max_sent_len = max_sent_len
        self.summary_len = summary_len
        self.min_summary_char_len = min_summary_char_len

        self.articles = {}
        self.summaries = {}

    def get_summaries(self):
        return self.summaries if self.summaries else self._create_summaries()

    def get_articles(self):
        return self.articles if self.articles else self._collect_articles(self.keywords)

    def _collect_articles(self, keywords):
        articles = {}
        for kw in keywords:
            try:
                articles[kw] = self._scrape_text(kw)
            except HTTPError:
                continue
        self.articles = articles
        return articles

    def _scrape_text(self, keyword):
        article = urllib.request.urlopen(
            f'https://en.wikipedia.org/wiki/{keyword}').read()
        parsed_article = bs.BeautifulSoup(article, 'lxml')
        paragraphs = parsed_article.find_all('p')

        text = ""
        for p in paragraphs:
            text += p.text

        return text

    def _get_summarizer(self, text):
        if self.summarizer == "cluster":
            return ClusterSummary(text, self.min_word_freq, self.dist_metric, self.n_clusters, self.lang)
        elif self.summarizer == "freq":
            return MostFrequentSummary(text, self.max_sent_len, self.summary_len, self.lang)

    def _create_summaries(self):
        articles = self.get_articles()
        for kw in self.keywords:
            summarizer = self._get_summarizer(articles[kw])
            self.summaries[kw] = summarizer.get_summary()
        summaries = {keyword: summary for keyword, summary in self.summaries.items(
        ) if len(summary) >= self.min_summary_char_len}
        self.summaries = summaries
        return self.summaries
