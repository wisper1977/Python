# Description: Module to create a dialog window for changing ping settings.

import tkinter as tk
from tkinter import simpledialog, Label, Entry, messagebox
from modules.log_manager import LogManager   

class PingSettingsDialog(simpledialog.Dialog):
    def __init__(self, master, config_manager):
        """PingSettingsDialog constructor to initialize the dialog window."""
        self.logger = LogManager.get_instance()
        try:
            self.config_manager = config_manager
            self.num_attempts = int(self.config_manager.get_setting('PING', 'attempts', '5'))
            self.timeout_duration = int(self.config_manager.get_setting('PING', 'timeout', '15'))
            super().__init__(master, title="Ping Settings")
            self.logger.log_info("PingSettingsDialog initialized successfully")
        except Exception as e:
            self.logger.log_error("Failed to initialize PingSettingsDialog: " + str(e))
            raise e

    def body(self, master):
        """Build the body of the dialog with input fields for settings."""
        try:
            Label(master, text="Number of Attempts:").grid(row=0, column=0)
            self.num_attempts_var = tk.StringVar(value=str(self.num_attempts))
            self.num_attempts_entry = Entry(master, textvariable=self.num_attempts_var)
            self.num_attempts_entry.grid(row=0, column=1)
            Label(master, text="Timeout Duration (seconds):").grid(row=1, column=0)
            self.timeout_duration_var = tk.StringVar(value=str(self.timeout_duration))
            self.timeout_duration_entry = Entry(master, textvariable=self.timeout_duration_var)
            self.timeout_duration_entry.grid(row=1, column=1)
            return self.num_attempts_entry
        except Exception as e:
            self.logger.log_error("Failed to create body for PingSettingsDialog: " + str(e))
            raise e

    def apply(self):
        """Apply the changes made in the dialog to the configuration file."""
        try:
            num_attempts = int(self.num_attempts_var.get())
            timeout_duration = int(self.timeout_duration_var.get())
            if num_attempts > 10:
                messagebox.showerror("Invalid Input", "Number of attempts cannot exceed 10.")
                self.logger.log_error("Number of attempts cannot exceed 10.")
                return
            # Save settings using the new method
            self.config_manager.save_settings('PING', 'attempts', num_attempts)
            self.config_manager.save_settings('PING', 'timeout', timeout_duration)
            self.logger.log_info("Ping settings updated from settings dialog.")
        except Exception as e:
            self.logger.log_error("Failed to apply changes in PingSettingsDialog: " + str(e))
            raise e