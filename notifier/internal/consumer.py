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
                body = json.dumps(payload, indent=2)

                email_sender.send(subject, body)
                EVENTS_SENT.labels(event_type=event_type).inc()

                logger.info("notification sent for event %s", event_type)
