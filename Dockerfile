FROM python:3.8.4

WORKDIR /pollingTool

COPY . .


RUN apt update

RUN pip install -r requirements.txt