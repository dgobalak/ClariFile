from flask import flash, request
from werkzeug.utils import secure_filename

from .parser import Parser
from .topic_selector import TopicSelector
from .wiki_summarizer import WikiSummarizer

import os


def get_summary_data(app) -> dict:
    fname = save_file(app)
    data = process_file(app, fname)
    delete_file(app, fname)

    return data


def save_file(app) -> str:
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        flash('No selected file')
        return ''

    if uploaded_file and allowed_file(uploaded_file.filename, app):
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename

    print("File type not supported.")
    return ''


def process_file(app, fname) -> dict:
    if fname != '':
        # Parse text from media file
        parser = Parser(os.path.join(app.config['UPLOAD_FOLDER'], fname))
        parsed_text = parser.get_text()

        # Extract keywords from text
        topic_selector = TopicSelector(text=parsed_text, lang="english")
        keywords = topic_selector.get_keywords()

        # Scrape wikipedia summary for each keyword
        wiki_summarizer = WikiSummarizer(keywords=keywords, lang="english")
        # Dict containing keyword:summary pairs
        summaries = wiki_summarizer.get_summaries()

        return summaries

    return {}


def delete_file(app, fname) -> None:
    if fname != '':
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], fname))


# Check if file type is supported
def allowed_file(filename, app) -> bool:
    return '.' in filename and \
        filename[len(filename)-1-filename[::-1].index("."):] in app.config['UPLOAD_EXTENSIONS']
