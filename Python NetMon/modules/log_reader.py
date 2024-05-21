#   This module is responsible for reading the log file.

from pathlib import Path
from modules.log_manager import LogManager

class LogReader:
    def __init__(self, log_file_path):
        """Initialize the LogReader with a path to the log file."""
        self.logger = LogManager.get_instance()
        self.log_file_path = Path(log_file_path)

    def read_log_file(self):
        """Read the log file and return its content."""
        try:
            with open(self.log_file_path, "r") as file:
                return file.readlines()
        except FileNotFoundError:
            self.logger.log_error("Log file not found when trying to read log file.")
            return []
        except PermissionError:
            self.logger.log_error("Permission denied when trying to read log file.")
            return []
        except Exception as e:
            self.logger.log_error("Failed to read log file: " + str(e))
            return []