from flask import flash, request, sessions
from flask.app import Flask
from werkzeug.utils import secure_filename
from glob import glob

from .parser import Parser
from .topic_selector import TopicSelector
from .wiki_summarizer import WikiSummarizer
from .exceptions import NoKeywordsFoundException

import flask
import os
import sys

def get_summary_data(app: Flask, session: flask.session) -> dict:
    fname = ''
    data = {}

    try:
        fname = save_file(app)
        data = process_file(app, fname, session)
    except NoKeywordsFoundException as e:
        flash("No keywords found in file.")
        print(str(e), file=sys.stderr)
    except Exception as e:
        flash("Error occurred. Try again or use a different file.")
        print(str(e), file=sys.stderr)
    finally:
        delete_file(app, fname)

    return data


def save_file(app: Flask) -> str:
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        flash('No selected file')
        return ''

    if uploaded_file and allowed_file(uploaded_file.filename, app):
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename

    return ''


def process_file(app: Flask, fname: str, session: flask.session) -> dict:
    if fname != '':
        lang = session.get('language', '')
        summarizer = session.get('summarizer', '')
        cluster_dist = session.get('cluster-distance', '')
        summary_len = int(session.get('summary-length', -1))

        lang = lang.lower() if lang != '' else 'english'
        summarizer = summarizer.lower() if summarizer != '' else 'freq'
        cluster_dist = cluster_dist.lower() if cluster_dist != '' else 'cosine'
        summary_len = summary_len if summary_len > 0 else 8

        # Parse text from media file
        parser = Parser(os.path.join(app.config['UPLOAD_FOLDER'], fname))
        parsed_text = parser.get_text()

        # Extract keywords from text
        topic_selector = TopicSelector(text=parsed_text, lang="english")
        keywords = topic_selector.get_keywords()

        if len(keywords) == 0:
            raise NoKeywordsFoundException("No keywords found in file")

        # Scrape wikipedia summary for each keyword
        wiki_summarizer = WikiSummarizer(keywords=keywords, lang="english", summarizer=summarizer,
                                         dist_metric=cluster_dist, summary_len=summary_len, n_clusters=summary_len)

        # Dict containing keyword:summary pairs
        summaries = wiki_summarizer.get_summaries()

        return summaries

    return {}


def delete_file(app: Flask, fname: str) -> None:
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
    
    froot, _ = os.path.splitext(file_path)

    file_list = glob(froot + '.*')
    
    for file in file_list:
        if os.path.exists(file):
            os.remove(file)


# Check if file type is supported
def allowed_file(filename: str, app: Flask) -> bool:
    return '.' in filename and \
        filename[len(filename)-1-filename[::-1].index("."):] in app.config['UPLOAD_EXTENSIONS']
