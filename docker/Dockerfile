FROM python:3.7-bullseye
ARG API_VERSION=$API_VERSION
ENV API_VERSION=$API_VERSION
ADD requirements.txt /var/www/requirements.txt

RUN set -xe \
    && pip3 install -U pip \
    && pip3 install -r /var/www/requirements.txt

