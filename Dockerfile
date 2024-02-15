FROM python:3.8-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY .env.production .env

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
build-essential gcc libpq-dev libc-dev libmagic1 libpq5
RUN apt-get install libjemalloc2 && rm -rf /var/lib/apt/lists/*

ENV LD_PRELOAD /usr/lib/x86_64-linux-gnu/libjemalloc.so.2

COPY ./app /app

CMD ["echo", "start application"]