FROM python:3.11-slim

WORKDIR /app

ADD requirements.txt /app

RUN apt-get update && \
    apt-get upgrade && \
    apt-get install default-mysql-client && \
    pip install -r requirements.txt && \
    apt-get clean && \
    pip cache purge

CMD [ "python", "main.py" ]