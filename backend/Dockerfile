FROM python:3.11

RUN apt-get update && apt-get install -y \
    gettext \
    && apt-get clean


WORKDIR /code
COPY requirements/ /code/requirements/

RUN pip install -r requirements/prod.txt
COPY ./ /code/
WORKDIR /code/eco
ENV POSTGRES_USER=eco
ENV POSTGRES_PASSWORD=eco
ENV POSTGRES_DB=eco
ENV POSTGRES_HOST=db
ENV POSTGRES_PORT=5432
