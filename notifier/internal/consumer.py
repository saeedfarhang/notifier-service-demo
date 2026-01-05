import json
import logging
import aio_pika

from .filters import is_event_allowed
from .metrics import EVENTS_RECEIVED, EVENTS_SENT, DROPPED_ROUTING_KEY

logger = logging.getLogger("notifier.consumer")

async def consume(cfg: dict, email_sender):
    connection = await aio_pika.connect_robust(cfg["rabbitmq"]["url"])
    channel = await connection.channel()

    exchange = await channel.declare_exchange(
        cfg["rabbitmq"]["exchange"],
        aio_pika.ExchangeType.TOPIC,
        durable=False,
    )

    queue = await channel.declare_queue(
        cfg["rabbitmq"]["queue"],
        durable=False,
    )
    logger.info("Queue declared: %s", cfg["rabbitmq"]["queue"])
    
    for key in cfg["rabbitmq"]["routing_keys"]:
        await queue.bind(exchange, routing_key=key)
        
    allowed_routing_keys = set(cfg["rabbitmq"]["routing_keys"])

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                routing_key = message.routing_key
                if routing_key not in allowed_routing_keys:
                    DROPPED_ROUTING_KEY.labels(routing_key=routing_key or "unknown").inc()
                    logger.info("Dropped message due to routing key: %s", routing_key)
                    continue
                
                try:
                    payload = json.loads(json.loads(message.body).get("oslo.message", {}))
                except json.JSONDecodeError:
                    logger.error("Failed to parse message body as JSON: %s", message.body)
                    continue
                event_type = payload.get("event_type")
                logger.info("Event type: %s\nPayload: %s", event_type, payload)
                EVENTS_RECEIVED.labels(event_type=event_type).inc()
                if not is_event_allowed(event_type, cfg["events"]["allowed"]):
                    logger.info("Event not allowed: %s", event_type)
                    continue
                logger.info("Event allowed: %s", event_type)
                subject = f"[OpenStack] {event_type}"
                message = get_message_from_payload(payload)
                email_sender.send(subject, message)
                EVENTS_SENT.labels(event_type=event_type).inc()

                logger.info("notification sent for event %s", event_type)


def get_message_from_payload(payload):
    message = ""
    try:
        event = payload.get("event_type", "unknown")
        status = payload.get("payload", {}).get('message', None)
        display_name = payload.get("payload", {}).get('display_name', None)
        instance_id = payload.get("payload", {}).get('instance_id', None)
        
        if event == "compute.instance.create.start":
            message = f"creating instance {display_name} started."
        elif event == "compute.instance.create.end":
            message = f"creating instance {display_name} finished."
        elif event == "compute.instance.create.error":
            message = f"creating instance {display_name} has error."
        elif event == "compute.instance.delete.start":
            message = f"deleting instance {display_name} started."
        elif event == "compute.instance.delete.end":
            message = f"deleting instance {display_name} finished."
        elif event == "compute.instance.delete.error":
            message = f"deleting instance {display_name} has error."
        if status:
            message = f"{message} status: *{status}*"
        if instance_id:
            message = f"{message}\ninstance id: {instance_id}"
    except:
        body = json.dumps(payload, indent=2)
        message = body
    return message