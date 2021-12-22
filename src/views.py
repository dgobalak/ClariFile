from src import app
import os
from flask import render_template, redirect, url_for, flash, request, session
from .inc.files import get_summary_data


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = get_summary_data(app, session)
        if data != {}:  # File saved successfully
            return render_template("summaries.html", data=data)        
        else:
            return redirect(url_for("index"))

    return render_template("index.html")


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        form = request.form
        for key, value in form.items():
            if key == 'summary-length' and int(value) < 1:
                value = 1
            session[key] = value
        
        return redirect(url_for('index'))
            
    lang = session['language'] if session.get('language') else "English"
    summary_length = session['summary-length'] if session.get('summary-length') else 8
    cluster_distance = session['cluster-distance'] if session.get('cluster-distance') else "cosine"
    summarizer = session['summarizer'] if session.get('summarizer') else "freq"
    
    return render_template("settings.html", language=lang, summary_length=summary_length, cluster_distance=cluster_distance, summarizer=summarizer)


@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404
