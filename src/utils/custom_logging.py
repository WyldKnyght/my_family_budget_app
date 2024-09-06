# src/utils/custom_logging.py
import logging
import logging.config
import os
from rich.console import Console
from rich.theme import Theme
from typing import Any, Dict, Optional

# Constants for magic strings
LOG_ASCTIME = "asctime"
LOG_CREATED = "created"
LOG_LEVEL = "levelname"
LOG_NAME = "name"
LOG_MESSAGE = "message"

# Detailed logging format string (for debug level)
DETAILED_LOG_FORMAT = (
    f'{{ "{LOG_ASCTIME}":"%({LOG_ASCTIME})s", "{LOG_CREATED}":%({LOG_CREATED})f, '
    f'"{LOG_LEVEL}":"%({LOG_LEVEL})s", "{LOG_NAME}":"%({LOG_NAME})s", '
    f'"{LOG_MESSAGE}":"%({LOG_MESSAGE})s" }}'
)

# Simple logging format string (for info level and above)
SIMPLE_LOG_FORMAT = f'%({LOG_ASCTIME})s - %({LOG_LEVEL})s - %({LOG_MESSAGE})s'

# Default logging configuration
DEFAULT_LOGGING_CONFIG = {
    'level': 'DEBUG',
    'ring_buffer_capacity': 100,
}

# Module-specific logger
logger = logging.getLogger(__name__)

class RingBuffer(logging.StreamHandler):
    def __init__(self, capacity: int) -> None:
        super().__init__()
        self.capacity = capacity
        self.buffer = []
        self.detailed_formatter = logging.Formatter(DETAILED_LOG_FORMAT)
        self.simple_formatter = logging.Formatter(SIMPLE_LOG_FORMAT)

    def emit(self, record: logging.LogRecord) -> None:
        if record.levelno <= logging.DEBUG:
            msg = self.detailed_formatter.format(record)
        else:
            msg = self.simple_formatter.format(record)
        self.buffer.append(msg)
        if len(self.buffer) > self.capacity:
            self.buffer.pop(0)

    def get(self) -> list[str]:
        return self.buffer

class DetailedRichHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super().__init__(level)
        self.console = Console(
            log_time=True,
            log_time_format='%H:%M:%S-%f',
            theme=Theme(
                {
                    "traceback.border": "black",
                    "traceback.border.syntax_error": "black",
                    "inspect.value.border": "black",
                }
            ),
        )
        self.detailed_formatter = logging.Formatter(DETAILED_LOG_FORMAT)
        self.simple_formatter = logging.Formatter(SIMPLE_LOG_FORMAT)

    def emit(self, record):
        try:
            if record.levelno <= logging.DEBUG:
                message = self.detailed_formatter.format(record)
            else:
                message = self.simple_formatter.format(record)
            self.console.print(message, highlight=True)
        except Exception:
            self.handleError(record)

def setup_logging(config: Optional[Dict[str, Any]] = None) -> None:
    if config is None:
        config = DEFAULT_LOGGING_CONFIG

    # Dynamically set logging level from environment variables
    env_log_level = os.getenv("LOG_LEVEL", config['level'].upper())
    config['level'] = env_log_level

    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'detailed': {'format': DETAILED_LOG_FORMAT},
            'simple': {'format': SIMPLE_LOG_FORMAT},
        },
        'handlers': {
            'console': {
                'class': f'{__name__}.DetailedRichHandler',
                'level': config['level'],
            },
            'ring_buffer': {
                'class': f'{__name__}.RingBuffer',
                'capacity': config['ring_buffer_capacity'],
                'level': config['level'],
            },
        },
        'loggers': {
            '': {  # Root logger
                'handlers': ['console', 'ring_buffer'],
                'level': config['level'],
            },
        },
    }

    logging.config.dictConfig(logging_config)

    # Suppress unnecessary logging from other libraries
    libraries_to_suppress = ["urllib3", "httpx", "diffusers", "torch"]
    for library in libraries_to_suppress:
        logging.getLogger(library).setLevel(logging.ERROR)