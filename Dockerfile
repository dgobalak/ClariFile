FROM python:3.8

LABEL maintainer="dgobalak@uwaterloo.ca"

ENV DEBIAN_FRONTEND=noninteractive

# define the present working directory
WORKDIR /File-Insights

# add the contents into the working dir
COPY . /File-Insights

# run pip to install the dependencies of the flask app
RUN pip install -r requirements.txt

# Update apt-get
RUN apt-get update -y

# install required dependencies for textract
RUN apt-get install -y python-dev unrtf poppler-utils tesseract-ocr \
flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig

# download all nltk data
RUN python -m nltk.downloader -d /usr/local/nltk_data all

# define the command to start the container
ENTRYPOINT ["python","run.py"]