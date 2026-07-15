import logging
import sys

import structlog 

def configure_logging() -> None:
    """
    Configures logging for the application.
    Sets up both standard logging and structlog for structured logging.
    """

    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)
    
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.PrintLoggerFactory()
    )