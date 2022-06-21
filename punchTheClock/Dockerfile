FROM python:3.10-alpine

# set work directory
WORKDIR /usr/src/app
COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies for cffi and psycopg2
RUN apk update && \
    apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev postgresql-dev gcc musl-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh


ENTRYPOINT ["/bin/sh", "/usr/src/app/entrypoint.sh"]