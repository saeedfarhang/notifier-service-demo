def is_event_allowed(event_type: str, allowed_events: list[str]) -> bool:
    return event_type in allowed_events
