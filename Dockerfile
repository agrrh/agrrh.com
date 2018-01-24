FROM python:3-slim as agrrhbuilder

RUN apt update -qq && apt install python-pip -qqy
RUN pip install pelican

COPY . /source

WORKDIR /source
RUN pwd
RUN ls -l .
RUN pelican -o /site /source
RUN ls -l /source
RUN ls -l /site

FROM nginx:alpine

COPY --from=agrrhbuilder /site /usr/share/nginx/html
RUN ls -l /site
