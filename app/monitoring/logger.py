import logging
import json
import sys

logger = logging.getLogger("llm_platform")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if hasattr(record, "extra_data"):
            log_record.update(record.extra_data)
        return json.dumps(log_record)


handler.setFormatter(JsonFormatter())
logger.addHandler(handler)
