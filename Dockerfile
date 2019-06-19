FROM python:3.7-alpine

WORKDIR /app

ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache bash git

COPY Pipfile* /app/

RUN pip install pipenv

RUN pipenv install --system --deploy --dev

COPY . .

CMD python .
