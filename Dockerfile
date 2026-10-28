FROM python:3.10-slim-bullseye 

WORKDIR /frontend

COPY frontend/requirements.txt /frontend/requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5000

COPY frontend/src/ /frontend

ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
CMD ["newrelic-admin", "run-program", "flask", "run", "--host=0.0.0.0", "-p", "5000"]
