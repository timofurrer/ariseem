FROM python:3.6-alpine
MAINTAINER Timo Furrer <tuxtimo@gmail.com>

EXPOSE 5000

WORKDIR /app

VOLUME ["/app"]

COPY . /app

RUN pip install .

ENV FLASK_APP ariseem/__main__.py
ENV FLASK_DEBUG 1
ENV ARISEEM_CONFIG ./config.yml

CMD ["flask", "run", "--host=0.0.0.0"]
