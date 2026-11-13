# One Dockerfile, three images. Pick the flavor with --target:
#   plain     no agent
#   newrelic  New Relic Python agent (newrelic-admin)
#   otel      OpenTelemetry auto-instrumentation (opentelemetry-instrument)
FROM python:3.10-slim-bullseye AS base
# Optional: trust an extra CA (for local builds behind TLS inspection). Pass it with
#   docker build --secret id=extra_ca,src=ca.pem ...
# Does nothing when the secret is absent, so CI builds are unaffected.
RUN --mount=type=secret,id=extra_ca \
    if [ -s /run/secrets/extra_ca ]; then \
      cp /run/secrets/extra_ca /usr/local/share/ca-certificates/extra-ca.crt && update-ca-certificates \
      && pip3 config --global set global.cert /etc/ssl/certs/ca-certificates.crt; \
    fi
WORKDIR /frontend
COPY frontend/requirements.txt /frontend/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 5000

FROM base AS plain
COPY frontend/src/ /frontend
CMD ["flask", "run", "--host=0.0.0.0", "-p", "5000"]

FROM base AS newrelic
COPY frontend/requirements-newrelic.txt /frontend/requirements-newrelic.txt
RUN pip3 install --no-cache-dir -r requirements-newrelic.txt
COPY frontend/src/ /frontend
ENV NEW_RELIC_APP_NAME=doodle-frontend \
    NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
CMD ["newrelic-admin", "run-program", "flask", "run", "--host=0.0.0.0", "-p", "5000"]

FROM base AS otel
COPY frontend/requirements-otel.txt /frontend/requirements-otel.txt
RUN pip3 install --no-cache-dir -r requirements-otel.txt \
 && opentelemetry-bootstrap -a install
COPY frontend/src/ /frontend
ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
CMD ["opentelemetry-instrument", "flask", "run", "--host=0.0.0.0", "-p", "5000"]
