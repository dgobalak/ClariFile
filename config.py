import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode. Set to False if converting to GUI
DEBUG = True

# Secret key for session management. You can generate random strings here:
# https://randomkeygen.com/
SECRET_KEY = '6cOGFyylnBYVNs012bS4gjtWfsfds3423w3eqfea3d977d588'

# File upload settings
UPLOAD_EXTENSIONS = ['.wav', '.mp3', 'mp4', '.png', '.pdf']
UPLOAD_FOLDER = "temp_storage/"
# MAX_CONTENT_LENGTH = 1024 * 1024


# Connect to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False