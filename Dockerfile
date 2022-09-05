FROM python:3-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt update
RUN apt install -y libpq-dev gcc

WORKDIR /datasaver
COPY requirements.txt /datasaver/
RUN pip install -r requirements.txt
COPY . /datasaver/
RUN DJANGO_SECRET_KEY=x python3 manage.py collectstatic --no-input

EXPOSE 8000

ENTRYPOINT gunicorn -w 4 -b 0.0.0.0:8000 datasaver_proj.wsgi:application