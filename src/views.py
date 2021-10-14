from src import app
from flask import render_template, redirect, url_for, flash, request


@app.route('/')
def index():
    return render_template("index.html")


@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404