FROM python:3.8.5-alpine3.12

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev libffi jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev make

RUN pip install --upgrade pip

RUN mkdir /code

COPY requirements.txt /code

RUN pip install -r /code/requirements.txt

COPY . /code

WORKDIR /code
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
# CMD python /code/manage.py runserver 0:8000

