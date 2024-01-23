FROM python:3.9.14-alpine


WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev libc-dev \
    && apk add postgresql postgresql-dev \
    && apk add jpeg-dev zlib-dev libjpeg libffi-dev cairo-dev pango-dev gdk-pixbuf-dev

RUN pip install --upgrade pip

COPY BlogApp/ .flake8 requirements.txt /usr/src/app/

RUN pip install -r /usr/src/app/requirements.txt

RUN mkdir -p /usr/src/app/static
