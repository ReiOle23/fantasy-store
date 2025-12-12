FROM python:3.12.3

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /app
COPY . .

RUN apt-get update -y
RUN apt-get install gettext build-essential -y

RUN pip3.12 install -r requirements.txt

