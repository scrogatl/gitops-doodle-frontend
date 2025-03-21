FROM python:3.10-slim-bullseye 

WORKDIR /frontend

COPY frontend/requirements.txt /frontend/requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5000

COPY frontend/src/ /frontend
CMD flask run --host=0.0.0.0 -p 5000
# CMD newrelic-admin run-program flask run --host=0.0.0.0 -p 5000
# CMD opentelemetry-instrument --logs_exporter otlp flask run --debugger --host=0.0.0.0 -p 5000