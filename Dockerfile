FROM python:3-slim as builder

WORKDIR /source
RUN apt update -qq && apt install python-pip -qqy
COPY ./requirements.txt /source/requirements.txt
RUN pip install -r requirements.txt
COPY . /source
RUN pelican -d -o /site .

FROM nginx:alpine

COPY --from=builder --chown=nginx /site /usr/share/nginx/html
