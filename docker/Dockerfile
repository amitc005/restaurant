FROM python:3.6.8-slim-stretch
LABEL maintainer="Amit Chavhan <amitc005@gmail.com>"

RUN apt-get update && apt-get install -y vim
RUN mkdir /usr/local/fueled_project/
WORKDIR /usr/local/fueled_project/

COPY requirements.txt /usr/local/fueled_project/
RUN pip install -r requirements.txt

COPY . /usr/local/fueled_project/
