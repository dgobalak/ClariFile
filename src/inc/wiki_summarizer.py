from src.inc.text_summary import TextSummary
from urllib.error import HTTPError
import urllib.request
import bs4 as bs

class WikiSummarizer():
    def __init__(self, keywords, max_sent_len=30, summary_len=8, lang='english'):
        self.keywords = keywords
        self.max_sent_len = max_sent_len
        self.summary_len = summary_len
        self.lang = lang

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
        article = urllib.request.urlopen(f'https://en.wikipedia.org/wiki/{keyword}').read()
        parsed_article = bs.BeautifulSoup(article,'lxml')
        paragraphs = parsed_article.find_all('p')
        
        text = ""
        for p in paragraphs:
            text += p.text

        return text

    def _create_summaries(self):
        articles = self.get_articles()
        for kw in self.keywords:
            summary = TextSummary(articles[kw], self.max_sent_len, self.summary_len, self.lang)
            self.summaries[kw] = summary.get_summary()
        
        return self.summaries
