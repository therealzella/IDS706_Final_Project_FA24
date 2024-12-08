import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logger(service_name):
    """Setup logger with proper format and rotating file handler"""
    # Create logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Configure logging
    logger = logging.getLogger(service_name)
    logger.setLevel(logging.INFO)

    # Create handlers
    file_handler = RotatingFileHandler(
        f"logs/{service_name}.log", maxBytes=1024 * 1024, backupCount=5  # 1MB
    )
    console_handler = logging.StreamHandler()

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Add formatter to handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
