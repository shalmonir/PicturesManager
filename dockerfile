# syntax=docker/dockerfile:1

FROM python:3.7-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt

RUN apt-get update
RUN apt-get -y install curl
RUN apt-get install -y libpq-dev gcc
RUN export PATH=/usr/lib/postgresql/X.Y/bin/:$PATH
RUN apt-get install -y python3-dev
RUN apt-get install -y python3-psycopg2

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD gunicorn --bind 0.0.0.0:5000 app:app

