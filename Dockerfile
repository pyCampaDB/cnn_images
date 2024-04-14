
#Use the official image of Python
FROM python:3.11.0-slim

#Establised your work directory
WORKDIR /app

#Install pipenv
RUN pip install pipenv

#Copy our Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock /app/

#Installing depends in the system
RUN pipenv install --system --deploy

#Copy all the files
COPY . /app

#Expose the port 8888
EXPOSE 8888

ENV NAME PipEnvironment

CMD pipenv run python pipenvDockerGit.py
    