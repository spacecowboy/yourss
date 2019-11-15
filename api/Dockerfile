FROM python:3.6-slim-stretch
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y gcc libpq-dev libxml2-dev
ENV PYTHONBUFFERED 1
COPY ./requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code
WORKDIR /code
EXPOSE 6543


RUN pip install --editable .