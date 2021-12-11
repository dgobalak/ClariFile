from src import app
import os
from flask import render_template, redirect, url_for, flash, request
from .inc.files import get_summary_data


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = get_summary_data(app)
        print(data)
        if data != {}:  # File saved successfully
            return redirect(url_for('index'))
        else:
            return redirect(request.url)

    return render_template("index.html")


@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404
