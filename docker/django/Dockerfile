FROM python:3.9-alpine3.13

ENV PYTHONUNBUFFERED 1



COPY ./requirements.txt /tmp/requirements.txt
COPY . .
WORKDIR /core
EXPOSE 8000
RUN pip install --upgrade pip && \
    apk update && \
    apk add --no-cache \
        postgresql-client \
        postgresql-dev \
        gcc \
        python3-dev \
        musl-dev \
        libffi-dev && \
    pip install wait-for-it && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser --disabled-password --no-create-home django-user


USER django-user
