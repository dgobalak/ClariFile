import os
import tempfile
import pytest

from flask import session
from tests import app

@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            pass
        yield client

    os.unlink(app.config['DATABASE'])


def change_settings(client, language, summary_length, summarizer, cluster_distance):
    return client.post('/settings', data=dict(
        language=language,
        summary_length=summary_length,
        summarizer=summarizer,
        cluster_distance=cluster_distance
    ), follow_redirects=True)


def test_settings_change():
    with app.test_client() as c:
        language = "English"
        summary_length = "8"
        summarizer = "freq"
        cluster_distance = "cosine"
        change_settings(c, language, summary_length,
                        summarizer, cluster_distance)
        
        assert session['language'] == language and session['summary_length'] == summary_length and session[
            'summarizer'] == summarizer and session['cluster_distance'] == cluster_distance

        language = "English"
        summary_length = "3"
        summarizer = "cluster"
        cluster_distance = "euclidean"
        change_settings(c, language, summary_length,
                        summarizer, cluster_distance)
        
        assert session['language'] == language and session['summary_length'] == summary_length and session[
            'summarizer'] == summarizer and session['cluster_distance'] == cluster_distance

        language = "English"
        summary_length = "15"
        summarizer = "freq"
        cluster_distance = "euclidean"
        change_settings(c, language, summary_length,
                        summarizer, cluster_distance)
        
        assert session['language'] == language and session['summary_length'] == summary_length and session[
            'summarizer'] == summarizer and session['cluster_distance'] == cluster_distance


def test_homepage_content():
    with app.test_client() as c:
        rv = c.get('/')
        assert b'An open source web application that provides insight into media content' in rv.data
        assert b'Drag and drop a file or select add File' in rv.data
        assert b'Text Extraction' in rv.data
        assert b'Keyword Identification' in rv.data
        assert b'Wiki Summarization' in rv.data
