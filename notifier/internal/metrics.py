from prometheus_client import Counter, start_http_server

EVENTS_RECEIVED = Counter(
    "openstack_events_received_total",
    "Total OpenStack events received",
    ["event_type"],
)

EVENTS_SENT = Counter(
    "openstack_notifications_sent_total",
    "Notifications sent",
    ["event_type"],
)

DROPPED_ROUTING_KEY = Counter(
    "openstack_notifications_dropped_routing_key_total",
    "Messages dropped due to unexpected routing key",
    ["routing_key"],
)

def start_metrics_server(addr: str, port: int):
    start_http_server(port, addr)
