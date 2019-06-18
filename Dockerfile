FROM python:3.7-alpine

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY Pipfile* /app/

RUN apk add --no-cache bash git

RUN pip install pipenv && pipenv install --system

# Install service
COPY . .

CMD python .
