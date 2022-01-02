from src.inc.freq_summary import MostFrequentSummary
from src.inc.cluster_summary import ClusterSummary
from src.inc.lang_detection_utils import *
from src.inc.translator import Translator
from urllib.error import HTTPError
from typing import Union
import urllib.request
import bs4 as bs


class WikiSummarizer():
    def __init__(self,
                 keywords: set,
                 summarizer: str = "freq",
                 dist_metric: str = "cosine",
                 n_clusters: int = 8,
                 max_sent_len: int = 30,
                 summary_len: int = 8,
                 lang: str = 'auto',
                 min_summary_char_len: int = 100,
                 target: Union[str, None] = None
                 ) -> None:

        self.keywords = keywords
        self.lang = detect_lang(" ".join(keywords)) if lang == 'auto' else lang
        self.summarizer = summarizer
        self.target = target

        # Cluster summary config
        self.dist_metric = dist_metric
        self.n_clusters = n_clusters

        # Frequency summary config
        self.max_sent_len = max_sent_len
        self.summary_len = summary_len
        self.min_summary_char_len = min_summary_char_len

        self.articles = {}
        self.summaries = {}

    def get_summaries(self) -> dict:
        return self.summaries if self.summaries else self._create_summaries()

    def get_articles(self) -> dict:
        return self.articles if self.articles else self._collect_articles(self.keywords)

    def _collect_articles(self, keywords: set) -> dict:
        articles = {}
        new_keywords = []
        for kw in keywords:
            try:
                articles[kw] = self._scrape_text(kw)
                new_keywords.append(kw)
            except HTTPError:
                continue
        self.articles = articles
        self.keywords = new_keywords
        return articles

    def _scrape_text(self, keyword: str) -> str:
        kw = "_".join(keyword.split())
        article = urllib.request.urlopen(
            f'https://en.wikipedia.org/wiki/{kw}').read()
        parsed_article = bs.BeautifulSoup(article, 'lxml')
        paragraphs = parsed_article.find_all('p')

        text = ""
        for p in paragraphs:
            text += p.text

        return text

    def _get_summarizer(self, text: str, failed: bool = False) -> Union[ClusterSummary, MostFrequentSummary]:
        summarizer = self.summarizer

        if failed:
            if self.summarizer == "cluster":
                summarizer = "freq"
            else:
                summarizer = "cluster"

        if summarizer == "cluster":
            return ClusterSummary(text, self.dist_metric, self.n_clusters, self.lang)
        elif summarizer == "freq":
            return MostFrequentSummary(text, self.max_sent_len, self.summary_len, self.lang)

    def _create_summaries(self) -> dict:
        articles = self.get_articles()
        for kw in self.keywords:
            summarizer = self._get_summarizer(articles[kw])

            try:
                summary = summarizer.get_summary()
            except:
                summarizer = self._get_summarizer(articles[kw], True)
                summary = summarizer.get_summary()

            # Translate text if a target lang is specified
            if self.target:
                summary = Translator(summary, self.target).translate()
            self.summaries[kw] = summary

        summaries = {keyword: summary for keyword, summary in self.summaries.items(
        ) if len(summary) >= self.min_summary_char_len}
        self.summaries = summaries
        return self.summaries
