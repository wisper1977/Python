# Description: Main entry point for the application.
# Version: 1.1.3.1

# Import required libraries
import tkinter as tk
from modules.log_manager import LogManager
from modules.application import Application

if __name__ == "__main__":
    """Main entry point for the application."""
    log_manager = LogManager.get_instance()
    log_manager.log_info("Application started")
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    log_manager.log_info("Application ended")
