FROM python:3.8.1
# define the present working directory
WORKDIR /File-Insights
# add the contents into the working dir
ADD . /File-Insights
COPY ./data/nltk_data /usr/local/nltk_data

# run pip to install the dependencies of the flask app
RUN pip install -r requirements.txt

# define the command to start the container
ENTRYPOINT ["python","run.py"]