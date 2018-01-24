FROM python:3-slim as builder

RUN apt update -qq && apt install python-pip -qqy
RUN pip install pelican

ADD . /source

WORKDIR /source
RUN pelican -o /site

# ---

FROM alpine:latest

VOLUME /site
WORKDIR /site
COPY --from=builder /site .

CMD tail -f /dev/null
