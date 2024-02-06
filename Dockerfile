FROM python:3.8-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY .env.production .env

COPY ./app /app
