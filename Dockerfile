FROM python:3.8-slim-buster

ENV FLASK_APP=falk
ENV FLASK_CONFIG=default
ENV DATABASE_URL = mysql+mysqlconnector://dev:1234@127.0.0.1/falk


RUN adduser -D falk
USER falk

WORKDIR /home/falk

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY falk.py config.py boot.sh ./

EXPOSE 5000
ENTRYPOINT [ "./boot.sh" ]