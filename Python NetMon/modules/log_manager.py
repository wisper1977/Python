# Description: This module contains the LogManager class which is a singleton class that provides logging functionality for the application.

from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

class LogManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        """Get the singleton instance of the LogManager class."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """Initialize the LogManager instance with a rotating file handler."""
        try:
            if LogManager._instance is not None:
                raise Exception("This class is a singleton!")
            else:
                LogManager._instance = self
            self.setup_logging()
        except Exception as e:
            logging.error(f"Error initializing LogManager: {e}")
            raise e

    def setup_logging(self):
        """Setup logging configuration for the application."""
        try:
            log_directory = Path('log')
            log_directory.mkdir(exist_ok=True)
            log_file_path = log_directory / 'log_file.txt'
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5),
                    logging.StreamHandler()
                ]
            )
        except Exception as e:
            logging.error(f"Error setting up logging: {e}")
            raise e
        
    def log_info(self, message):
        """Log an info message."""
        try:
            logging.info(message)
        except Exception as e:
            logging.error(f"Error logging info message: {e}")
            raise e

    def log_debug(self, message):
        """Log a debug message."""
        try:
            logging.debug(message)
        except Exception as e:
            logging.error(f"Error logging debug message: {e}")
            raise e

    def log_warning(self, message):
        """Log a warning message."""
        try:
            logging.warning(message)
        except Exception as e:
            logging.error(f"Error logging warning message: {e}")
            raise e

    def log_error(self, message):
        """Log an error message and raise an exception."""
        try:
            logging.error(message)
        except Exception as e:
            logging.error(f"Error logging error message: {e}")
            raise e

    def log_critical(self, message):
        """Log a critical message and raise an exception."""
        try:
            logging.critical(message)
        except Exception as e:
            logging.error(f"Error logging critical message: {e}")
            raise e