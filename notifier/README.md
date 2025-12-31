# Notifier Service

Python service that listens to OpenStack notifications on RabbitMQ, filters events, sends email alerts, and exposes Prometheus metrics.

## Flow

- OpenStack services publish events to RabbitMQ exchanges (e.g., `openstack` with routing keys `notifications.*`).
- Notifier binds to the configured routing keys, parses messages, and checks against the allowed event list.
- Allowed events generate an email notification and increment Prometheus counters.

## components

- `cmd/notifier/main.py` -- entrypoint: loads config, starts metrics server (optional), and runs the consumer.
- `internal/consumer.py` -- connects to RabbitMQ, binds queue/routing keys, parses messages, filters events, triggers email, updates metrics.
- `internal/email.py` -- SMTP sender; can be disabled for dry runs.
- `internal/filters.py` -- simple allowlist check for event types.
- `internal/metrics.py` -- Prometheus counters for received/sent events, metrics server bootstrap.
- `internal/config.py` -- YAML loader.
- `internal/logging.py` -- basic logging setup.

## Configuration

Default file: `configs/config.yaml`

```yaml
rabbitmq:
  url: amqp://user:pass@host:5672/
  exchange: openstack
  queue: notifications.info
  routing_keys:
    - notifications.info
    - notifications.error

email:
  enabled: false
  smtp_host: smtp.gmail.com
  smtp_port: 587
  username: notifier@example.com
  password: password
  from: notifier@example.com
  to:
    - admin@example.com

events:
  allowed:
    - compute.instance.create.end
    - compute.instance.create.error

metrics:
  enabled: true
  listen_addr: 0.0.0.0
  port: 9000
```

> Provide credentials via env vars (or a secrets manager) and render the config at runtime; keep the repo sample non-sensitive.

## Running

```bash
cd notifier
python -m venv env && source env/bin/activate
pip install -r requirements.txt
python -m cmd.notifier.main configs/config.yaml
```

Metrics exposed at `http://<host>:9000/metrics` when enabled.

## troubleshooting

- Logging is stdout-based; include `event_type` and payload in INFO logs.
- RabbitMQ connection uses `aio_pika.connect_robust`; it will attempt to reconnect if the broker restarts.
- For email issues, set `email.enabled=true`, verify STARTTLS reachability to `smtp_host:smtp_port`, and check for auth errors in logs.

## Design notes / outstanding improvements

- Parsing: current implementation `json.loads(json.loads(message.body).get("oslo.message", {}))` assumes the OpenStack Oslo envelope; consider hardening for malformed payloads.
- Resilience: add per-event retries/backoff and dead-letter handling for email failures.
- Observability: add counters for parse failures and email errors; expose a health endpoint.
