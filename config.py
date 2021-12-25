import os
import datetime

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

SECRET_KEY = os.urandom(24).hex()
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=365)

# File upload settings
UPLOAD_EXTENSIONS = ['.wav', '.mp3', '.mp4', '.mov',
                     '.pdf', '.jpg', '.png', '.txt', '.jpeg', '.html']
UPLOAD_FOLDER = "temp_storage/"

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
