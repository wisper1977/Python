# Description: Main entry point for the application.
# Version: 1.1.3.1

# Import required libraries
import tkinter as tk
from modules.log_manager import LogManager
from modules.application import Application
from modules.config_manager import ConfigManager

if __name__ == "__main__":
    """Main entry point for the application."""
    config_manager = ConfigManager()  # Create ConfigManager instance first
    log_manager = LogManager.get_instance(config_manager)  # Pass ConfigManager instance here
    config_manager.set_logger(log_manager)  # Set LogManager instance in ConfigManager
    log_manager.log_info("Application started")
    root = tk.Tk()
    app = Application(master=root, config_manager=config_manager, log_manager=log_manager)
    app.mainloop()
    log_manager.log_info("Application ended")