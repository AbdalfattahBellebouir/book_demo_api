import logging
import structlog
# from ddtrace import tracer
import sys

# def inject_trace_ids(logger, method_name, event_dict):
#     span = tracer.current_span()
#     if span:
#         event_dict["dd.trace_id"] = span.trace_id
#         event_dict["dd.span_id"] = span.span_id
#     return event_dict

def setup_structlog():
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    structlog.configure(
        processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        # inject_trace_ids,
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
    )
