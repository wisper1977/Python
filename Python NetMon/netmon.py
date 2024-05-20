# Version: 1.1.3

# Import required libraries
import configparser, csv, subprocess, logging, re, winsound
import platform, webbrowser, os, winsound
import tkinter as tk
from pathlib import Path
from tkinter import ttk, simpledialog, Label, Entry, messagebox, scrolledtext
from logging.handlers import RotatingFileHandler
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from shutil import move

# Define global variables
version = "1.1.3"
hyperlink = "https://tinyurl.com/PyNetMon"
developer = "Chris Collins"
log_directory = Path("log")
log_file_path = log_directory / 'log_file.txt'
archive_directory = log_directory / 'archive'

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

class LogViewerGUI:
    def __init__(self, master, app):
        self.logger = LogManager.get_instance() # Get the singleton instance of LogManager
        self.master = master # Reference to the main application window
        self.app = app # Reference to the main application class to access business logic
        self.log_reader = LogReader(log_file_path)
        self.log_writer = LogWriter(log_file_path)
        self.last_archive_time = datetime.now()  # Initialize the last archive time
     
    def update_log_display(self):
        """Update the log content in the log viewer."""
        try:
            with open(log_file_path, 'r') as log_file:
                log_content = log_file.readlines()

            # Filter the logs by the selected log level
            log_level = self.log_level.get()
            if log_level != "ALL":
                log_content = [line for line in log_content if log_level in line]

            self.log_text.delete('1.0', tk.END)  # Clear the current log content
            self.log_text.insert(tk.END, ''.join(log_content))  # Insert the new log content
        except FileNotFoundError:
            self.logger.log_error("Log file not found, creating a new one.")
            with open('log_file.txt', "w") as file:
                pass
        except PermissionError:
            self.logger.log_error("Permission denied when trying to update log display.")
            messagebox.showerror("Error", "Permission denied when trying to update log display.")
        except Exception as e:
            self.logger.log_error("Failed to update log display: " + str(e))
            messagebox.showerror("Error", "Failed to update log display: " + str(e))
             
    def open_log_viewer(self):
        """Open a new window to display logs."""
        try:
            log_window = tk.Toplevel(self.master)
            log_window.attributes('-topmost', True)  # Keep the window on top
            log_window.title("Log Viewer")  # Set the title of the log window

            # Create a menu bar
            menubar = tk.Menu(log_window)
            log_window.config(menu=menubar)

            # Create a log menu and add it to the menu bar
            log_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Logs", menu=log_menu)

            # Add "Refresh Logs" and "Clear Logs" options to the log menu
            log_menu.add_command(label="Refresh Logs", command=self.update_log_display)
            log_menu.add_command(label="Clear Logs", command=lambda: self.clear_log_confirmation(self.log_text))

            # Create a dropdown menu to select the log level
            self.log_level = tk.StringVar(log_window)
            self.log_level.set("ALL")  # default value
            log_level_options = ["ALL", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            log_level_dropdown = tk.OptionMenu(log_window, self.log_level, *log_level_options, command=lambda _: self.update_log_display())
            log_level_dropdown.pack()

            # Create a ScrolledText widget for log display in the new window
            self.log_text = scrolledtext.ScrolledText(log_window, height=20, width=80)
            self.log_text.pack(padx=10, pady=10, fill='both', expand=True)

            self.update_log_display()  # Initialize with log content
            self.auto_refresh_log_display()  # Start auto-refresh
        except FileNotFoundError:
            self.logger.log_error("Log file not found when trying to open log viewer.")
            messagebox.showerror("Error", "Log file not found when trying to open log viewer.")
            return
        except PermissionError:
            self.logger.log_error("Permission denied when trying to open log viewer.")
            messagebox.showerror("Error", "Permission denied when trying to open log viewer.")
            return
        except Exception as e:
            self.logger.log_error("Failed to open log viewer: " + str(e))
            messagebox.showerror("Error", "Failed to open log viewer: " + str(e))
            return
        
    def clear_log_confirmation(self, log_text_widget):
        """Ask for confirmation before clearing logs."""
        try:
            if messagebox.askyesno("Clear Logs", "Are you sure you want to clear all logs?"):
                self.log_writer.clear_logs(log_text_widget)
        except PermissionError:
            self.logger.log_error("Permission denied when trying to clear logs.")
            messagebox.showerror("Error", "Permission denied when trying to clear logs.")
        except FileNotFoundError:
            self.logger.log_error("Log file not found when trying to clear logs.")
            messagebox.showerror("Error", "Log file not found when trying to clear logs.")
        except Exception as e:
            self.logger.log_error("Failed to clear logs: " + str(e))
            raise e
                
    def auto_refresh_log_display(self):
        """Auto refresh the log content."""
        try:
            self.update_log_display()
            self.log_text.after(120000, self.auto_refresh_log_display)
            print("Current time: ", datetime.now())
            print("Last archive time: ", self.last_archive_time)
            print("Time delta: ", timedelta(hours=24))
            if datetime.now() - self.last_archive_time >= timedelta(hours=24):  # If it's been 24 hours since the last archive
                self.archive_logs()  # Archive the current log file
            self.logger.log_info("Log display auto-refreshed.")
        except PermissionError:
            self.logger.log_error("Permission denied when trying to auto refresh log display.")
            messagebox.showerror("Error", "Permission denied when trying to auto refresh log display.")
        except FileNotFoundError:
            self.logger.log_error("Log file not found when trying to auto refresh log display.")
            messagebox.showerror("Error", "Log file not found when trying to auto refresh log display.")
        except Exception as e:
            self.logger.log_error("Failed to auto refresh log display: " + str(e))
            raise e

class LogReader:
    def __init__(self, log_file_path):
        """Initialize the LogReader with a path to the log file."""
        self.logger = LogManager.get_instance()
        self.log_file_path = log_file_path

    def read_log_file(self):
        """Read the log file and return its content."""
        try:
            with open(log_directory / 'log_file.txt', "r") as file:
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

class LogWriter:
    def __init__(self, log_file_path):
        """Initialize the LogWriter with a path to the log file."""
        self.logger = LogManager.get_instance()
        self.log_file_path = log_file_path

    def clear_logs(self, log_text_widget):
        """Clears the log file and updates the display."""
        try:
            self.logger.log_info("Attempting to archive logs...")
            self.archive_logs()  # Archive the current log file before clearing
            self.logger.log_info("Logs archived successfully.")

            self.logger.log_info("Attempting to clear log file...")
            with open(log_directory / 'log_file.txt', "w") as file:
                file.truncate()  # Clear the file content
            self.logger.log_info("Log file cleared successfully.")

            self.logger.log_info("Attempting to clear log text widget...")
            log_text_widget.delete(1.0, tk.END)  # Clear the text widget
            self.logger.log_info("Log text widget cleared successfully.")

            self.logger.log_info("Log file cleared by user.")
        except PermissionError:
            self.logger.log_error("Permission denied when trying to clear logs.")
            messagebox.showerror("Error", "Permission denied when trying to clear logs.")
        except FileNotFoundError:
            self.logger.log_error("Log file not found when trying to clear logs.")
            messagebox.showerror("Error", "Log file not found when trying to clear logs.")
        except Exception as e:
            self.logger.log_error("Failed to clear log file: " + str(e))
            messagebox.showerror("Error", "Failed to clear logs: " + str(e))

    def archive_logs(self):
        """Archive the current log file."""
        for i in range(3):  # try 3 times
            try:
                archive_directory.mkdir(parents=True, exist_ok=True)  # Ensure the archive directory exists
                if log_file_path.exists():
                    # Remove the logger
                    logging.shutdown()

                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    archive_file_path = archive_directory / f'log_file_{timestamp}.txt'
                    move(log_file_path, archive_file_path)

                    # Use the logger from LogManager
                    self.logger = LogManager.get_instance()

                    self.logger.log_info(f"Archived log file to {archive_file_path} by the system")
                    self.last_archive_time = datetime.now()  # Update the last archive time
                break
            except PermissionError as e:
                if i < 2:  # if it's not the last try
                    time.sleep(1)  # wait for 1 second
                else:  # if it's the last try
                    self.logger.log_error(f"Error archiving log file: {e}")
                    raise  # re-raise the last exception
            except FileNotFoundError as e:
                self.logger.log_error(f"Log file not found when trying to archive: {e}")
                raise e
            except Exception as e:
                self.logger.log_error(f"Error archiving log file: {e}")
                raise e
     
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
            if not os.path.exists(self.config_path):
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
        
class DeviceFileHandler:
    def __init__(self, filepath):
        """Initialize the DeviceFileHandler with a filepath and LogManager instance."""
        try:
            self.filepath = Path(filepath)
            self.logger = LogManager.get_instance()
            self.initialize_device_file()
        except Exception as e:
            self.logger.log_error(f"Failed to initialize DeviceFileHandler: {e}")
            raise e

    def initialize_device_file(self):
        """Initialize the device file with a header if it doesn't exist."""
        try:
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            if not self.filepath.exists():
                with open(self.filepath, mode='w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=["Key", "Location", "Name", "IP", "Type", "Status", "Acknowledge"])
                    writer.writeheader()
                self.logger.log_info("Device file created with header.")
            else:
                # Check file integrity upon initialization
                if not self.check_file_integrity():
                    # Log and raise an exception if file integrity check fails
                    self.logger.log_warning("Device file integrity check failed upon initialization.")
                    raise IOError("Device file integrity check failed.")
        except IOError as e:
            self.logger.log_error(f"Failed to create or access device file: {e}")
            raise e

    def check_file_integrity(self):
        """Check if the device file has the required fields in the header."""
        try:
            with open(self.filepath, mode='r', newline='') as file:
                reader = csv.reader(file)
                header = next(reader)
                required_fields = ["Key", "Location", "Name", "IP", "Type", "Status"]
                # Check if header contains all required fields
                if not all(field in header for field in required_fields):
                    return False
            return True
        except Exception as e:
            self.logger.log_error(f"Error while checking device file integrity: {e}")
            return False

    def read_devices(self):
        """Read the devices from the device file and return as a list of dictionaries."""
        try:
            with open(self.filepath, mode='r', newline='') as file:
                return list(csv.DictReader(file))
        except IOError as e:
            self.logger.log_error(f"Failed to read device file: {e}")
            raise e

    def write_devices(self, devices):
        """Write the list of devices to the device file."""
        try:
            with open(self.filepath, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["Key", "Location", "Name", "IP", "Type", "Status", "Acknowledge"])
                writer.writeheader()
                writer.writerows(devices)
            self.logger.log_debug("Device file updated successfully.")
        except IOError as e:
            self.logger.log_error(f"Failed to write to device file: {e}")
            raise e

class DeviceManager:
    def __init__(self, filepath='config/equipment.csv'):
        """Initialize the DeviceManager with a DeviceFileHandler and LogManager."""
        try:
            self.filepath = filepath  # store filepath as an instance variable
            self.file_handler = DeviceFileHandler(filepath)
            self.logger = LogManager.get_instance()
            self.devices = self.load_devices()
        except Exception as e:
            self.logger.log_error(f"Failed to initialize DeviceManager: {e}")
            raise e

    def load_devices(self):
        """Load the devices from the device file."""
        try:
            return self.file_handler.read_devices()
        except Exception as e:
            self.logger.log_error(f"Failed to load devices: {e}")
            return []

    def save_device(self, device):
        """Save a new device to the device file."""
        try:
            devices = self.load_devices()
            # Ensure uniqueness of keys
            new_key = self.generate_new_key(devices)
            device['Key'] = str(new_key)
            devices.append(device)
            self.file_handler.write_devices(devices)
        except Exception as e:
            self.logger.log_error(f"Failed to save device: {e}")

    def delete_device(self, device_key):
        """Delete a device with the given key from the device file."""
        try:
            devices = self.load_devices()
            original_count = len(devices)
            devices = [device for device in devices if device['Key'] != str(device_key)]
            if len(devices) == original_count:
                self.logger.log_warning(f"No device found with Key: {device_key} to delete.")
            else:
                self.logger.log_info(f"Device with Key: {device_key} deleted.")
                self.file_handler.write_devices(devices)
        except Exception as e:
            self.logger.log_error(f"Failed to delete device: {e}")

    def update_device(self, device_key, new_details):
        """Update the details of a device with the given key."""
        try:
            devices = self.load_devices()
            for device in devices:
                if device['Key'] == str(device_key):
                    device.update(new_details)
            self.file_handler.write_devices(devices)
        except Exception as e:
            self.logger.log_error(f"Failed to update device: {e}")

    def update_acknowledge_status(self, device_key, status):
        """Update the acknowledge status of a device."""
        try:
            # Read the CSV file into a list of rows
            with open(self.filepath, 'r') as file:
                reader = csv.reader(file)
                data = list(reader)

            # Find the row with the device key and update the status
            for row in data:
                if row[0] == device_key:  # assuming the device key is in the 1st column
                    row[6] = status  # assuming the acknowledge status is in the 7th column
                    self.logger.log_info(f"Device with Key {device_key} acknowledged.")
                    break  # exit the loop once the device key is found

            # Write the updated data back to the CSV file
            with open(self.filepath, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)
                self.logger.log_info(f"Acknowledge status updated for device with Key: {device_key} in CSV file.")

            self.logger.log_info(f"Acknowledge status updated for device with Key: {device_key}")
        except Exception as e:
            self.logger.log_error(f"Failed to update acknowledge status: {e}")
            return e

    def generate_new_key(self, devices=None):
        """Generate a new unique key for a device based on existing keys."""
        try:
            max_key = max((int(device['Key']) for device in devices), default=0)
            return max_key + 1
        except Exception as e:
            self.logger.log_error(f"Failed to generate new key: {e}")
            return 1  # Default to 1 if key generation fails

class DeviceDialog(simpledialog.Dialog):
    def __init__(self, master, existing_details=None, action=None):
        """DeviceDialog constructor to initialize the dialog window."""
        self.logger = LogManager.get_instance()
        try:
            self.existing_details = existing_details or {'Key': '', 'Location': '', 'Name': '', 'IP': '', 'Type': '', 'Status': 'Unknown'}
            self.action = action
            super().__init__(master, title="Edit Device Details" if existing_details else "Add Device Details")
            self.logger.log_info("DeviceDialog initialized successfully")
        except Exception as e:
            self.logger.log_error("Failed to initialize DeviceDialog: " + str(e))
            raise e

    def body(self, master):
        """Build the body of the dialog with input fields for device details."""
        try:
            Label(master, text="Key:").grid(row=0, column=0)
            Label(master, text="Location:").grid(row=1, column=0)
            Label(master, text="Name:").grid(row=2, column=0)
            Label(master, text="IP:").grid(row=3, column=0)
            Label(master, text="Type:").grid(row=4, column=0)
            self.key_var = tk.StringVar(master, self.existing_details['Key'])
            self.location_var = tk.StringVar(master, self.existing_details['Location'])
            self.name_var = tk.StringVar(master, self.existing_details['Name'])
            self.ip_var = tk.StringVar(master, self.existing_details['IP'])
            self.type_var = tk.StringVar(master, self.existing_details['Type'])
            key_entry = Entry(master, textvariable=self.key_var, state='readonly')
            key_entry.grid(row=0, column=1)
            location_entry = Entry(master, textvariable=self.location_var)
            location_entry.grid(row=1, column=1)
            name_entry = Entry(master, textvariable=self.name_var)
            name_entry.grid(row=2, column=1)
            ip_entry = Entry(master, textvariable=self.ip_var)
            ip_entry.grid(row=3, column=1)
            type_entry = Entry(master, textvariable=self.type_var)
            type_entry.grid(row=4, column=1)
            return key_entry
        except Exception as e:
            self.logger.log_error("Failed to create body for DeviceDialog: " + str(e))
            raise e

    def apply(self):
        """Apply the changes made in the dialog to the device details."""
        try:
            details = {
                'Key': self.key_var.get(),
                'Location': self.location_var.get(),
                'Name': self.name_var.get(),
                'IP': self.ip_var.get(),
                'Type': self.type_var.get(),
                'Status': 'Unknown'
            }
            if self.action:
                self.action(details)
            self.result = details
        except Exception as e:
            self.logger.log_error("Failed to apply changes in DeviceDialog: " + str(e))
            raise e
      
class NetworkOperations:
    def __init__(self, config, update_callback, max_workers=10):
        """Initialize the NetworkOperations class with a ThreadPoolExecutor."""
        try:
            self.config = config
            self.update_callback = update_callback
            self.executor = ThreadPoolExecutor(max_workers=max_workers)
            self.logger = LogManager.get_instance()
            self.logger.log_debug("NetworkOperations initialized with ThreadPoolExecutor.")
        except Exception as e:
            self.logger.log_error(f"Failed to initialize NetworkOperations: {e}")
            raise e

    def ping_device(self, ip):
        """Submit a ping task to the ThreadPoolExecutor for the given IP address."""
        try:
            future = self.executor.submit(self._ping, ip)
            future.add_done_callback(lambda x: self.process_ping_result(x, ip))
        except Exception as e:
            self.logger.log_error(f"Error submitting ping task for device {ip}: {e}")
            self.update_callback(ip, "Error: Failed to submit ping task")

    def _ping(self, ip):
        """Perform a ping operation on the given IP address."""
        try:
            self.logger.log_info(f"Pinging device with IP: {ip}")
            attempts = int(self.config.get_setting('PING', 'attempts', '3'))
            timeout = int(self.config.get_setting('PING', 'timeout', '100'))
            command = self._construct_ping_command(ip, attempts, timeout)
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
            return result
        except subprocess.TimeoutExpired:
            return "Offline, Ping Timeout"
        except subprocess.CalledProcessError as e:
            self.logger.log_error(f"Error pinging {ip}: {e}")
            return f"Offline, Ping Error: {e}"
        except Exception as e:
            self.logger.log_error(f"Unexpected error pinging {ip}: {e}")
            return f"Offline, Unexpected Error: {e}"

    def process_ping_result(self, future, ip):
        """Process the result of the ping operation and update the device status."""
        try:
            result = future.result()
            if isinstance(result, str):
                status = result
            else:
                if result.returncode == 0:
                    status = self._parse_ping_output(result.stdout)
                else:
                    status = "Offline, Host Unreachable" if "Destination Host Unreachable" in result.stdout else "Offline, Ping Failed"
            self.update_callback(ip, status)
            self.logger.log_info(f"Result for device with IP {ip}: {status}")
        except Exception as e:
            self.logger.log_error(f"Error processing ping result for device {ip}: {e}")
            self.update_callback(ip, "Error: Failed to process ping result")

    def _construct_ping_command(self, ip, attempts, timeout):
        """Construct the ping command based on the OS."""
        try:
            if platform.system() == 'Windows':
                return ['ping', '-n', str(attempts), '-w', str(timeout * 1000), ip]
            else:
                return ['ping', '-c', str(attempts), '-W', str(timeout), ip]
        except Exception as e:
            self.logger.log_error(f"Error constructing ping command: {e}")
            return []

    def _parse_ping_output(self, output):
        """Parse the output of the ping command to extract the average time."""
        try:
            ping_lines = output.splitlines()
            time_matches = [re.search(r'time=(\d+)ms', line) for line in ping_lines]
            times = [float(match.group(1)) for match in time_matches if match]
            if times:
                avg_time = sum(times) / len(times)
                return f"Online, Avg ping: {avg_time:.2f} ms"
            return "Online, No time reported"
        except Exception as e:
            self.logger.log_error(f"Error parsing ping output: {e}")
            return "Online, Error parsing ping output"
   
    def shutdown(self):
        """Shutdown the ThreadPoolExecutor for network operations."""
        try:
            self.executor.shutdown(wait=False)
            self.logger.log_info("NetworkOperations shutdown initiated.")
        except Exception as e:
            self.logger.log_error(f"Error shutting down NetworkOperations: {e}")

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

class ApplicationGUI:
    def __init__(self, master, app):
        """Initialize the GUI with a reference to the main application and device manager."""
        self.logger = LogManager.get_instance()
        self.master = master
        self.app = app  # Reference to the main application class to access business logic
        self.log_viewer = LogViewerGUI(master, app)  # Initialize the log viewer window
        self.device_manager = DeviceManager()
        try:
            self.create_menu()
            self.create_widgets()
            self.load_devices()
        except Exception as e:
            self.logger.log_error("Failed to initialize GUI: " + str(e))
            raise e

    def create_menu(self):
        """Create the menu bar with File, Edit, View, and Help menus."""
        try:
            # Create the menu bar
            menubar = tk.Menu(self.master)
            file_menu = tk.Menu(menubar, tearoff=0)
            edit_menu = tk.Menu(menubar, tearoff=0)
            view_menu = tk.Menu(menubar, tearoff=0)
            help_menu = tk.Menu(menubar, tearoff=0)
            
            # Adding 'Settings' under 'File'
            file_menu.add_command(label="Settings", accelerator="Ctrl+S", command=self.open_settings)
            file_menu.add_separator()
            file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.quit_app)
            
            # Adding 'Add Device', 'Edit Device', and 'Delete Device' under 'Edit'
            edit_menu.add_command(label="Add Device", accelerator="Ctrl+A", command=self.add_device)
            edit_menu.add_command(label="Edit Device", accelerator="Ctrl+E", command=self.edit_device)
            edit_menu.add_command(label="Delete Device", accelerator="Ctrl+D", command=self.delete_device)
            
            # Adding 'Log' under 'View'
            view_menu.add_command(label="View Log", command=self.log_viewer.open_log_viewer)
        
            # Adding 'Online Help' and 'About' under 'Help'
            help_menu.add_command(label="Online Help", accelerator="Ctrl+H", command=self.open_online_help)
            help_menu.add_command(label="About", accelerator="Ctrl+I", command=self.show_about)
            
            # Binding keyboard shortcuts to menu items
            self.master.bind("<Control-s>", lambda event: self.open_settings())
            self.master.bind("<Control-q>", lambda event: self.quit_app())
            self.master.bind("<Control-a>", lambda event: self.add_device())
            self.master.bind("<Control-e>", lambda event: self.edit_device())
            self.master.bind("<Control-d>", lambda event: self.delete_device())
            self.master.bind("<Control-h>", lambda event: self.open_online_help())
            self.master.bind("<Control-i>", lambda event: self.show_about())

            # Adding the menus to the menubar
            menubar.add_cascade(label="File", menu=file_menu)
            menubar.add_cascade(label="Edit", menu=edit_menu)
            menubar.add_cascade(label="View", menu=view_menu)
            menubar.add_cascade(label="Help", menu=help_menu)
            self.master.config(menu=menubar)
        except Exception as e:
            self.logger.log_error("Failed to create menu: " + str(e))
            raise e

    def create_widgets(self):
        """Create the main widgets for the application."""
        try:
            self.tree = ttk.Treeview(self.master, columns=("Key", "Location", "Name", "IP", "Type", "Status", "Acknowledge"), show="headings")
            for col in ["Key", "Location", "Name", "IP", "Type", "Status", "Acknowledge"]:
                self.tree.heading(col, text=col)
                self.tree.column(col, anchor="center")
            self.tree.heading("Key", text="Key")
            self.tree.column("Key", width=0, stretch=tk.NO, minwidth=0)
            self.master.iconbitmap('media/NetMon.ico') 
            self.tree.grid(sticky='nsew', padx=10, pady=10)
            self.master.grid_rowconfigure(0, weight=1)
        
            self.tree.bind("<Double-1>", self.on_double_click)

            # Timer label
            self.timer_label = tk.Label(self.master, text="")
            self.timer_label.grid(sticky='ew', padx=10, pady=10)
            self.master.grid_rowconfigure(1, weight=0)
            self.master.grid_columnconfigure(0, weight=1)
            
        except Exception as e:
            self.logger.log_error("Failed to create widgets: " + str(e))
            raise e

    def on_double_click(self, event):
        """Handle double click event on a device."""
        try:
            item = self.tree.selection()
            if item:
                device_key = self.tree.item(item, "values")[0]
                device_status = self.tree.item(item, "values")[5]
                if device_status.startswith('Offline'):
                    # Update acknowledgment status in GUI
                    self.tree.set(item, column='Acknowledge', value='✔')
                    # Update acknowledgment status in CSV file
                    self.app.device_manager.update_acknowledge_status(device_key, 'True')             
                else:
                    # Log warning if the device cannot be acknowledged
                    LogManager.get_instance().log_warning(f"Device with Key {device_key} cannot be acknowledged as it is not offline.")
        except Exception as e:
            self.logger.log_error("Failed to handle double click event: " + str(e))
            raise e

    def add_device(self):
        """Open a dialog to add a new device and save it to the device file."""
        try:
            dialog = DeviceDialog(self.master)
            if dialog.result:
                new_device = dialog.result
                new_key = self.device_manager.generate_new_key()
                new_device['Key'] = str(new_key)
                self.device_manager.save_device(new_device)
                self.load_devices()
        except Exception as e:
            self.logger.log_error("Failed to add device: " + str(e))
            raise e

    def edit_device(self):
        """Open a dialog to edit an existing device and save the changes to the device file."""
        try:
            selected_item = self.tree.selection()
            if selected_item:
                item = self.tree.item(selected_item[0], "values")
                if item:
                    existing_details = {
                        'Key': item[0],
                        'Location': item[1],
                        'Name': item[2],
                        'IP': item[3],
                        'Type': item[4],
                        'Status': item[5]
                    }
                    dialog = DeviceDialog(self.master, existing_details=existing_details)
                    if dialog.result:
                        # If the IP has changed, update the device with the new details
                        if dialog.result['IP'] != existing_details['IP']:
                            self.device_manager.update_device(dialog.result['Key'], dialog.result)
                        else:
                            # If the IP has not changed, update the device without changing the status
                            dialog.result['Status'] = existing_details['Status']
                            self.device_manager.update_device(dialog.result['Key'], dialog.result)
                        self.load_devices()
        except Exception as e:
            self.logger.log_error("Failed to edit device: " + str(e))
            raise e

    def delete_device(self):
        """Delete the selected device from the device file."""
        try:
            selected_item = self.tree.selection()
            if selected_item:
                item = self.tree.item(selected_item[0])
                device_key = item['values'][0]  # Assuming 'Key' is the first column in values
                response = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the device with Key: {device_key}?")
                if response:
                    self.device_manager.delete_device(device_key)
                    self.load_devices()
        except Exception as e:
            self.logger.log_error("Failed to delete device: " + str(e))
            raise e

    def load_devices(self):
        """Load devices from the device file and populate the TreeView."""
        try:
            # Clear the TreeView
            for i in self.tree.get_children():
                self.tree.delete(i)

            # Load devices from the device file
            devices = self.device_manager.load_devices()

            # Populate the TreeView with devices
            for device in devices:
                # Convert the 'Acknowledge' field to a checkmark or blank
                acknowledge = '✔' if device['Acknowledge'] == 'True' else ''
                self.tree.insert('', 'end', values=(device['Key'], device['Location'], device['Name'], device['IP'], device['Type'], device['Status'], acknowledge))
        except Exception as e:
            self.logger.log_error("Failed to load devices: " + str(e))
            raise e

    def initiate_refresh_cycle(self):
        """Initialize the refresh cycle with dynamic interval based on ping attempts."""
        try:
            self.refresh_network_status()
        except Exception as e:
            self.logger.log_error("Failed to initiate refresh cycle: " + str(e))
            raise e

    def update_refresh_interval(self):
        """Update the refresh interval based on the number of ping attempts."""
        try:
            interval = int(self.config_manager.get_setting('DEFAULT', 'refreshinterval', '30'))
            self.after(interval * 1000, self.refresh_network_status)
        except Exception as e:
            self.logger.log_error("Failed to update refresh interval: " + str(e))
            raise e

    def refresh_network_status(self):
        """Refresh the network status of all devices periodically."""
        try:
            ping_attempts = int(self.app.config_manager.get_setting('PING', 'attempts', '5'))
            if ping_attempts <= 5:
                interval = 60  # Refresh every 60 seconds if attempts are 5 or fewer
            elif 6 <= ping_attempts <= 10:
                interval = 90  # Refresh every 90 seconds if attempts are between 6 and 10
            else:
                interval = 90  # Cap at 90 seconds for more than 10 attempts
                ping_attempts = 10  # Cap the number of attempts at 10
                self.config_manager.save_settings('PING', 'attempts', '10')  # Save capped value

            self.update_device_statuses()
            self.countdown = interval
            self.update_timer_label()
            self.master.after(interval * 1000, self.refresh_network_status)
        except Exception as e:
            self.logger.log_error("Failed to refresh network status: " + str(e))
            raise e

    def update_device_statuses(self):
        """Update the status of each device by sending ping requests."""
        try:
            devices = self.device_manager.load_devices()
            for device in devices:
                self.app.network_ops.ping_device(device['IP'])
        except Exception as e:
            self.logger.log_error("Failed to update device statuses: " + str(e))
            raise e

    def update_timer_label(self):
        """Update the timer label to show the countdown until the next refresh."""
        try:
            if self.countdown > 0:
                self.timer_label.config(text=f"Next update in {self.countdown} seconds")
                self.countdown -= 1
                self.master.after(1000, self.update_timer_label)  # Schedule the label to update in 1 second
            else:
                self.timer_label.config(text="Updating...")
        except Exception as e:
            self.logger.log_error("Failed to update timer label: " + str(e))
            raise e

    def sort_devices(self):
        """Sort devices by status, putting 'Offline' devices on top."""
        try:
            # Create a list of tuples (status, tree item id)
            l = [(self.tree.set(k, "Status"), k) for k in self.tree.get_children('')]
            # Sort so that 'Offline' comes first, followed by 'Online' and others
            l.sort(key=lambda t: (t[0] != "Offline", t))
            # Rearrange items in the treeview based on their new sort order
            for index, (val, k) in enumerate(l):
                self.tree.move(k, '', index)
        except Exception as e:
            self.logger.log_error("Failed to sort devices: " + str(e))
            raise e

    def open_settings(self):
        """Open the settings dialog to configure the refresh interval and ping settings."""
        try:
            dialog = PingSettingsDialog(self.master, self.app.config_manager)
            if dialog.result:
                self.refresh_network_status()  # Immediately refresh to apply new settings
        except Exception as e:
            self.logger.log_error("Failed to open settings dialog: " + str(e))
            raise e

    def open_online_help(self):
        """Open the online help page in the default web browser."""
        try:
            webbrowser.open_new_tab(hyperlink)
        except Exception as e:
            self.logger.log_error("Failed to open online help: " + str(e))
            raise e

    def show_about(self):
        """Display the 'About' dialog with information about the application."""
        try:
            messagebox.showinfo("About Python NetMon", f"Version: {version}\nDeveloped by: {developer}\nA simple network monitoring tool built with Python and Tkinter.")
        except Exception as e:
            self.logger.log_error("Failed to show about dialog: " + str(e))
            raise e

    def quit_app(self):
        """Quit the application and perform cleanup operations."""
        try:
            self.master.quit()
        except Exception as e:
            self.logger.log_error("Failed to quit application: " + str(e))
            raise e

class Application(tk.Frame):
    def __init__(self, master=None):
        """Initialize the main application with the root window and setup the GUI."""
        try:
            super().__init__(master)
            self.master = master
            self.master.title("Python NetMon")
            self.master.state('zoomed')
            
            self.setup_logging()
            self.config_manager = ConfigManager()
            self.device_manager = DeviceManager(filepath='config/equipment.csv')
            self.gui = ApplicationGUI(master, self)
            self.network_ops = self.setup_network_operations()

            self.gui.load_devices()
            self.gui.initiate_refresh_cycle()
        except Exception as e:
            self.logger.log_error("Failed to initialize application: " + str(e))
            raise e
   
    def setup_logging(self):
        """Setup logging configuration for the application."""
        try:
            self.logger = LogManager.get_instance()
            self.logger.log_debug("Application initializing...")
        except Exception as e:
            self.logger.log_error("Failed to setup logging: " + str(e))
            raise e

    def setup_network_operations(self):
        """Setup the NetworkOperations class with a callback to update the device status in the GUI."""
        try:
            update_callback = self.update_device_status  # Delegate to GUI
            return NetworkOperations(self.config_manager, update_callback)
        except Exception as e: 
            self.logger.log_error("Failed to setup NetworkOperations: " + str(e))
            raise e

    def setup_gui(self):
        """Setup the GUI for the application."""
        try:
            self.create_menu()
            self.create_widgets()
            self.pack(fill='both', expand=True)
        except Exception as e:
            self.logger.log_error("Failed to setup GUI: " + str(e))
            raise e

    def update_device_status(self, ip, status, acknowledge=''):
        """Update the status of a specific device in the TreeView."""
        def update():
            """Update the status of the device in the TreeView."""
            try:
                for item in self.gui.tree.get_children():
                    device = self.gui.tree.item(item)['values']
                    if len(device) < 7:
                        # Add the missing acknowledgement field
                        device.append('False')
                        LogManager.get_instance().log_error("Device list was too short, added missing acknowledgement field: " + str(device))
                    if device[3] == ip:
                        color = 'red' if status.startswith('Offline') else 'white'
                       
                        # Reset the acknowledgement to 'False' if the status starts with 'Online' and the acknowledgement is 'True'
                        if status.startswith('Online') and device[6] == 'True':
                            device[6] = 'False'
                        self.gui.tree.item(item, values=(device[0], device[1], device[2], device[3], device[4], status, device[6]), tags=(color,))
                        self.gui.tree.tag_configure(color, background=color)
                        self.gui.sort_devices()  
                        self.master.update_idletasks()  # Update the GUI immediately
                        
                        # Play sound if device goes offline and acknowledge field is not True
                        if status.startswith('Offline') and device[6] != '✔':
                            for _ in range(3):
                                winsound.PlaySound('media/alert.wav', winsound.SND_FILENAME)
                        
                        # Update status in CSV
                        data = []
                        with open('config/equipment.csv', 'r') as file:
                            reader = csv.reader(file)
                            for row in reader:
                                if len(row) < 7:
                                    # Add the missing acknowledgement field
                                    row.append('False')
                                    LogManager.get_instance().log_error("Row list was too short, added missing acknowledgement field: " + str(row))
                                if row[3] == ip:
                                    row[5] = status
                                    # Reset the acknowledge field to 'False' if the status starts with 'Online' and the acknowledgement is 'True'
                                    if status.startswith('Online') and row[6] == 'True':
                                        row[6] = 'False'
                                        self.logger.log_info(f"Device with IP {ip} status reset to 'Online' and Acknowledge set to 'False'")
                                data.append(row)
                        with open('config/equipment.csv', 'w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerows(data)
                        
                        # Update the GUI
                        for item in self.gui.tree.get_children():
                            device = self.gui.tree.item(item)['values']
                            if device[3] == ip:
                                device[6] = '' if status.startswith('Online') else device[6]
                                self.gui.tree.item(item, values=device)
            except Exception as e:
                LogManager.get_instance().log_error("Failed to update device status: " + str(e))
                return e

        # Schedule the update operation to run in the main GUI thread
        self.master.after(0, update)

if __name__ == "__main__":
    """Main entry point for the application."""
    log_manager = LogManager.get_instance()
    log_manager.log_info("Application started")
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    log_manager.log_info("Application ended")
