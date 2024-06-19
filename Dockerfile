FROM python:3.10-slim-bullseye as base

FROM base as builder

RUN apt update && apt install git python3-pip -y
RUN apt install bash -y
RUN apt autoremove

FROM base

WORKDIR /frontend

COPY frontend/requirements.txt /frontend/requirements.txt
RUN pip3 install -r requirements.txt

COPY frontend/src/ /frontend

EXPOSE 5000


RUN --mount=type=secret,id=NEW_RELIC_LICENSE_KEY \
  cat /run/secrets/NEW_RELIC_LICENSE_KEY
ENV NEW_RELIC_LICENSE_KEY=$NEW_RELIC_LICENSE_KEY
ENV NEW_RELIC_APP_NAME=doodle-frontend

CMD newrelic-admin run-program flask run --host=0.0.0.0 -p 5000