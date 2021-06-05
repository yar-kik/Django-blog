FROM python:3.8

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . ./app