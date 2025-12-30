import logging
import smtplib
from email.message import EmailMessage


logger = logging.getLogger("notifier.email")
class EmailSender:
    def __init__(self, config: dict):
        self.cfg = config

    def send(self, subject: str, body: str):
        if not self.cfg.get("enabled", False):
            logger.warning("Email sending is disabled")
            return

        msg = EmailMessage()
        msg["From"] = self.cfg["from"]
        msg["To"] = ", ".join(self.cfg["to"])
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP(self.cfg["smtp_host"], self.cfg["smtp_port"]) as s:
            s.starttls()
            logger.info("SMTP server started at %s:%s", self.cfg["smtp_host"], self.cfg["smtp_port"])
            s.login(self.cfg["username"], self.cfg["password"])
            logger.info("SMTP server logged in")
            s.send_message(msg)
            logger.info("Email sent")