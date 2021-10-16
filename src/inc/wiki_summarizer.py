from text_summarizer import TextSummarizer
from urllib.error import HTTPError
import urllib.request
import bs4 as bs


class WikiSummarizer(TextSummarizer):
    def __init__(self, keywords):
        super().__init__()
        self.keywords = keywords
        self.articles = None

        self._set_articles()
    
    def get_articles(self):
        if not self.articles:
            self._set_articles()
        return self.articles

    def _set_articles(self):
        articles = {}
        for kw in self.keywords:
            try:
                articles[kw] = self._scrape_text(kw)
            except HTTPError:
                continue
        self.articles = articles
    
    def _scrape_text(self, keyword):
        article = urllib.request.urlopen(f'https://en.wikipedia.org/wiki/{keyword}').read()
        parsed_article = bs.BeautifulSoup(article,'lxml')
        paragraphs = parsed_article.find_all('p')
        
        text = ""
        for p in paragraphs:
            text += p.text

        return text
