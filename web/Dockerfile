# pull official base image
FROM python:3.8.3-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV POETRY_VERSION 1.0.10
ENV POETRY_VIRTUALENVS_CREATE false

# install psycopg2 dependencies
RUN apt-get update \
  && apt-get -y install gcc postgresql netcat \
  && apt-get clean

# install dependencies
RUN pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION"
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install --no-interaction --no-ansi

COPY ./entrypoint.sh .

COPY ./entrypoint.sh .
RUN chmod +x entrypoint.sh
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
