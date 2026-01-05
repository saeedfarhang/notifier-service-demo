# Observability With Alloy And Grafana

to config Alloy for collecting logs and prometheus data, first we should install it on our machine:

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://apt.grafana.com/gpg.key \
  | sudo gpg --dearmor -o /etc/apt/keyrings/grafana.gpg

echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" \
  | sudo tee /etc/apt/sources.list.d/grafana.list

sudo apt update
sudo apt install alloy
```

### Verify installation

```bash
alloy --version
systemctl status alloy
```

### Configuration layout

for configuring layout, Alloy expects `/etc/alloy/config.alloy`. this is the minimal config for host metrics + logs:

```hcl
logging {
  level = "info"
}

prometheus.exporter.unix "host" {}

prometheus.scrape "host" {
  targets    = prometheus.exporter.unix.host.targets
  forward_to = [prometheus.remote_write.default.receiver]
}

prometheus.remote_write "default" {
  endpoint {
    url = "http://localhost:9090/api/v1/write"
  }
}

loki.source.file "logs" {
  targets = [
    {__path__ = "/var/log/syslog"},
    {__path__ = "/opt/stack/logs/*.log"},
  ]
  forward_to = [loki.write.default.receiver]
}

loki.write "default" {
  endpoint {
    url = "http://localhost:3100/loki/api/v1/push"
  }
}
```

### Start and enable Alloy

```bash
sudo systemctl enable alloy
sudo systemctl restart alloy
```

then

```bash
journalctl -u alloy -f
```
