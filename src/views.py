from src import app
import os
from flask import render_template, redirect, url_for, flash, request
from werkzeug.utils import secure_filename


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if uploaded_file and allowed_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))       
            return redirect(url_for('index'))
        else:
            print("File type not supported.")
    return render_template("index.html")


@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


# Check if file type is supported
def allowed_file(filename):
    return '.' in filename and \
        filename[len(filename) - 1 - filename[::-1].index("."):] in app.config['UPLOAD_EXTENSIONS']
