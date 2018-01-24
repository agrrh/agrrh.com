FROM python:3-slim as builder

RUN apt update -qq && apt install python-pip -qqy
RUN pip install pelican

ADD . /source

WORKDIR /source
RUN pelican -o /site /source

FROM nginx:alpine

COPY --from=builder /site /usr/share/nginx/html
