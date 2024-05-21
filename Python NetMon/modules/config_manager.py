# Description: Module to manage the configuration settings for the application.

import configparser
from pathlib import Path
from modules.log_manager import LogManager

class ConfigManager:
    """Class to manage the configuration settings for the application."""
    DEFAULT_CONFIG = {
        'DEFAULT': {
            'refreshinterval': '30',
            'logfile': 'device_status_log.txt'
        },
        'PING': {
            'attempts': '3',
            'timeout': '15'
        }
    }

    def __init__(self, config_path='config/config.ini'):
        """Initialize the ConfigManager with a path to the configuration file."""
        self.logger = LogManager.get_instance()
        self.logger.log_debug("Initializing ConfigManager")
        self.config_path = Path(config_path)
        self.config = configparser.ConfigParser()

        try:
            self.load_or_create_config()
        except Exception as e:
            self.logger.log_critical(f"Unexpected error during configuration initialization: {e}")

    def load_or_create_config(self):
        """Load the configuration file if it exists, otherwise create a new one."""
        try:
            if not self.config_path.exists():
                self.create_default_config()
            else:
                try:
                    self.load_config()
                except Exception as e:
                    self.logger.log_error(f"Error loading configuration file: {e}")
                    self.logger.log_warning("Using default settings due to configuration file error.")
                    self.use_default_config()
        except Exception as e:
            self.logger.log_critical(f"Error loading or creating configuration file: {e}")
            raise e
                  
    def create_default_config(self):
        """Create a new configuration file with default settings if it doesn't exist."""
        try:
            self.config.read_dict(ConfigManager.DEFAULT_CONFIG)
            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)
            self.logger.log_info("No config file found. Created a new one with default settings.")
        except configparser.Error as e:
            self.logger.log_error(f"Configuration parsing error while creating default config: {e}")
            raise e
        except Exception as e:
            self.logger.log_critical(f"Unexpected error during default configuration creation: {e}")
            raise e

    def load_config(self):
        """Load the configuration file from disk."""
        try:
            self.config.read(self.config_path)
            self.logger.log_info("Config file loaded successfully.")
        except configparser.ParsingError as e:
            self.logger.log_error(f"Configuration parsing error: {e}")
        except Exception as e:
            self.logger.log_critical(f"Unexpected error during configuration reading: {e}")

    def use_default_config(self):
        """Use the default configuration settings if the file is missing or corrupted."""
        try:
            self.config.read_dict(ConfigManager.DEFAULT_CONFIG)
        except configparser.Error as e:
            self.logger.log_error(f"Configuration parsing error while using default config: {e}")
            raise e
        except Exception as e:
            self.logger.log_critical(f"Unexpected error using default configuration: {e}")
            raise e
        
    def save_settings(self, section, setting, value):
        """Save a setting to the configuration file."""
        try:
            if section not in self.config.sections() and section != 'DEFAULT':
                self.config.add_section(section)
            self.config.set(section, setting, str(value))
            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)
            self.logger.log_info(f"Config updated: [{section}] {setting} = {value}")
            self.load_config()  # Reload to apply changes
        except configparser.Error as e:
            self.logger.log_error(f"Configuration parsing error while saving settings: {e}")
        except Exception as e:
            self.logger.log_critical(f"Unexpected error while saving settings: {e}")

    def get_setting(self, section, option, fallback=None):
        """Get a setting from the configuration file with optional fallback value."""
        try:
            return self.config.get(section, option, fallback=fallback)
        except configparser.NoOptionError:
            self.logger.log_error(f"No option '{option}' in section '{section}'")
            return fallback
        except configparser.NoSectionError:
            self.logger.log_error(f"No section '{section}' found")
            return fallback
        except Exception as e:
            self.logger.log_error(f"Error retrieving setting: {e}")
            return fallback