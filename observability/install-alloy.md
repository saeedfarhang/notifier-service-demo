# Observability With Alloy And Grafana

to config Alloy for collecting logs and prometheus data, first we should install it on our machine:

```bash
sudo mkdir -p /etc/apt/keyrings/
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list

sudo apt-get update
sudo apt-get install alloy
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
  targets = prometheus.exporter.unix.host.targets

  forward_to = [prometheus.remote_write.default.receiver]
}


prometheus.scrape "notifier" {
  targets = [
    {
      __address__ = "127.0.0.1:9000",
      job         = "notifier",
    },
  ]

  forward_to = [prometheus.remote_write.default.receiver]
}


prometheus.remote_write "default" {
  endpoint {
    url = "http://localhost:9090/api/v1/write"
  }
}


loki.source.file "logs" {
  targets = [
    {
      __path__ = "/var/log/syslog",
      job      = "syslog",
      host     = "devstack-lab",
    },
    {
      __path__ = "/opt/stack/logs/*.log",
      job      = "devstack",
      host     = "devstack-lab",
    },
    {
      __path__ = "/opt/stack/notifier-service-demo/notifier/notifier.log",
      job      = "notifier",
      host     = "devstack-lab",
    },
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
