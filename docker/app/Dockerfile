# syntax=docker/dockerfile:1
FROM python:3-alpine
WORKDIR /usr/src/app
COPY ./src .
ENV FLASK_APP='app'
ENV JWT_SECRET='D=qw>e(`b1)^zx0'
ENV JWT_TOKEN_EXPIRES_IN_SECONDS='600'
ENV MAGNETO_PASSWORD='$2a$12$x8aEcXPpuqOK8.5X7JftbO84CJgk8WSzEJOQJC4i8T/ftXNubVE5K'
ENV DATABASE_HOST='localhost'
ENV DATABASE_PORT='5432'
ENV DATABASE_NAME='mutant_finder'
ENV DATABASE_USER='postgres'
ENV DATABASE_PASSWORD='postgres'
RUN apk add gcc
RUN apk add musl-dev
RUN apk add libffi-dev
RUN apk add postgresql-dev
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
ENTRYPOINT python -m gunicorn -w 1 -b 0.0.0.0:5000 app:app