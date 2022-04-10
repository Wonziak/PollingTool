FROM python:3.9.6-slim

WORKDIR /pollingTool

COPY . .


RUN apt update

RUN pip install -r requirements.txt