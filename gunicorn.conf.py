import os
import json
import logging
import sys

# from app.logging_config import JSONFormatter
# ===============================
#   GUNICORN CONFIGURATION
# ===============================

# Number of workers, log level, and bind host/port
# workers = int(os.getenv("GUNICORN_WORKERS", "2"))
# bind = os.getenv("GUNICORN_BIND", "0.0.0.0:5000")
loglevel = os.getenv("LOG_LEVEL", "info").lower()

# Log destinations: "-" means stdout/stderr
accesslog = os.getenv("ACCESS_LOG", "-")
errorlog = os.getenv("ERROR_LOG", "-")

# Make sure Gunicorn captures stdout/stderr from app logs
capture_output = True

# Use JSON formatting for both access and error logs
json_logging = os.getenv("JSON_LOGS", "true").lower() == "true"


# ===============================
#   JSON LOGGING FORMATTERS
# ===============================
#Trying Latest final
class JSONFormatter(logging.Formatter):
    """Custom JSON log formatter for structured logging."""
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "log_type": "gunicorn",
        }
        # Add optional metadata for request-based logs
        if hasattr(record, "request_id"):
            log_record["request_id"] = record.request_id
        if record.exc_info:
            log_record["error"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

# ===============================
#   FILTER: Skip health + metrics
# ===============================

class SkipEndpointsFilter(logging.Filter):
    """Skip logging for health and metrics endpoints."""
    def filter(self, record):
        msg = record.getMessage()
        return not (
            "/healthcheck" in msg or "/metrics" in msg
        )
    
    
def on_starting(server):
    # """Configure JSON logging globally when Gunicorn starts."""Older 0.3
    # if json_logging:
    #     formatter = JSONFormatter()

    #     # Replace Gunicorn error log handler
    #     if server.log.error_log:
    #         for handler in server.log.error_log.handlers:
    #             handler.setFormatter(formatter)

    #     # Replace access log handler
    #     if server.log.access_log:
    #         for handler in server.log.access_log.handlers:
    #             handler.setFormatter(formatter)

    if not json_logging:
        return

    formatter = JSONFormatter()

    # Error logs
    if server.log.error_log:
        for handler in server.log.error_log.handlers:
            handler.setFormatter(formatter)

    # Access logs + filter unwanted endpoints
    if server.log.access_log:
        for handler in server.log.access_log.handlers:
            handler.addFilter(SkipEndpointsFilter())
            handler.setFormatter(formatter)



# ===============================
#   ACCESS LOG FORMAT
# ===============================
# Keep access logs minimal for Loki ingestion
# Example JSON:
# {"timestamp": "...", "level": "INFO", "client":"127.0.0.1", "method":"GET", "path":"/api/v1/students", "status":200}
#Bad printing JSON
access_log_format = (
    '{"client":"%(h)s","user":"%(u)s","method":"%(m)s","path":"%(U)s","query":"%(q)s",'
    '"status":%(s)s,"size":%(B)s,"referer":"%(f)s","agent":"%(a)s","request_time":%(L)s}'
)

# access_log_format = (
#     '%(h)s %(l)s %(u)s "%(m)s %(U)s%(q)s" %(s)s %(B)s "%(f)s" "%(a)s" %(L)s'
# )
