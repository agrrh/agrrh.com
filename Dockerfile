FROM python:3-slim as builder

RUN apt update -qq && apt install python-pip -qqy
RUN pip install pelican

COPY . /source

WORKDIR /source
RUN pelican -o /site .
RUN ls -l /source/pages
RUN ls -l /site/pages

FROM nginx:alpine

COPY --from=builder --chown=nginx /site /usr/share/nginx/html
RUN ls -l /usr/share/nginx/html/pages
