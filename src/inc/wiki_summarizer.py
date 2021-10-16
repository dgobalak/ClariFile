from text_summarizer import TextSummarizer
import urllib.request
import bs4 as bs


class WikiSummarizer(TextSummarizer):
    def __init__(self):
        super().__init__()