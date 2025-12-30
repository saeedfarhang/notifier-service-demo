import asyncio
import logging
import sys

from internal.config import load_config
from internal.logging import setup_logging
from internal.email import EmailSender
from internal.consumer import consume
from internal.metrics import start_metrics_server


def main():
    setup_logging()
    logger = logging.getLogger("notifier.main")
    config_path = sys.argv[1] if len(sys.argv) > 1 else "configs/config.yaml"
    cfg = load_config(config_path)

    if cfg.get("metrics", {}).get("enabled"):
        logger.info("Starting metrics server")
        start_metrics_server(
            cfg["metrics"]["listen_addr"],
            cfg["metrics"]["port"],
        )
        logger.info("Metrics server started at %s:%s", cfg["metrics"]["listen_addr"], cfg["metrics"]["port"])

    email_sender = EmailSender(cfg["email"])
    asyncio.run(consume(cfg, email_sender))

if __name__ == "__main__":
    main()
