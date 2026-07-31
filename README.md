# GitOps Microservice Example

## This is the frontend for doodle

## Branches

- `main` — clean baseline; no OTel or New Relic instrumentation.
- `otel` — OpenTelemetry + New Relic NRDOT instrumentation, for Docker/Kubernetes deployments.
- `azure-functions-newrelic` — Azure Functions adapter (`azure-functions/`), instrumented with the New Relic Python agent. Branched from `main`.

### Note: The Helm charts are just for Argo deployment, not actually for Helm deployment

