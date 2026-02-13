from datetime import datetime

audit_log = []


def record_query_event(data: dict):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        **data,
    }
    audit_log.append(entry)
