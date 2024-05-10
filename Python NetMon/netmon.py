import configparser, csv, subprocess, platform, ipaddress, logging, queue, re, webbrowser
import tkinter as tk
from queue import Queue
from threading import Thread
from pathlib import Path
from tkinter import ttk, simpledialog, Label, Entry, messagebox
from logging.handlers import RotatingFileHandler

version = "1.1.1.1"
hyperlink = "https://tinyurl.com/PyNetMon"

class LogManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if LogManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            LogManager._instance = self
        self.setup_logging()

    def setup_logging(self):
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

    def log_info(self, message):
        logging.info(message)

    def log_debug(self, message):
        logging.debug(message)

    def log_warning(self, message):
        logging.warning(message)

    def log_error(self, message):
        logging.error(message)

    def log_critical(self, message):
        logging.critical(message)

class ConfigManager:
    def __init__(self, config_path='config/config.ini'):
        self.logger = LogManager.get_instance()
        self.config_path = Path(config_path)
        self.config = configparser.ConfigParser()
        try:
            self.load_config()
        except configparser.Error as e:
            self.logger.log_error(f"Configuration parsing error: {e}")
        except FileNotFoundError:
            self.logger.log_error("Configuration file not found, using default settings.")
            self.use_default_config()
        except Exception as e:
            self.logger.log_critical(f"Unexpected error during configuration initialization: {e}")

    def load_config(self):
        if not self.config_path.exists():
            self.config['PING'] = {'Attempts': '3', 'Timeout': '100'}
            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)
            self.logger.log_debug("No config file found. Created a new one with default settings.")
        else:
            self.config.read(self.config_path)
            self.logger.log_debug("Config file loaded successfully.")
        self.ping_attempts = self.config.getint('PING', 'Attempts')
        self.ping_timeout = self.config.getint('PING', 'Timeout')

    def save_settings(self, attempts, timeout):
        try:
            self.config.set('PING', 'Attempts', str(attempts))
            self.config.set('PING', 'Timeout', str(timeout))
            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)
            self.logger.log_debug(f"Settings saved: Attempts={attempts}, Timeout={timeout}")
        except IOError as e:
            self.logger.log_error(f"Failed to save settings: {e}")
        except configparser.Error as e:
            self.logger.log_error(f"Configuration error while saving settings: {e}")
        except Exception as e:
            self.logger.log_critical(f"Unexpected error while saving settings: {e}")

    def use_default_config(self):
        self.config['PING'] = {'Attempts': '3', 'Timeout': '100'}
        self.save_settings(3, 100)  # Save default settings

class DeviceManager:
    def __init__(self, filepath='config/equipment.csv'):
        self.logger = LogManager.get_instance()
        self.filepath = Path(filepath)
        try:
            if not self.filepath.exists():
                with open(self.filepath, mode='w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=["Key", "Location", "Name", "IP", "Type", "Status"])
                    writer.writeheader()
            self.logger.log_debug("DeviceManager initialized successfully")
        except IOError as e:
            self.logger.log_error(f"Failed to create device file: {e}")
        except Exception as e:
            self.logger.log_critical(f"Unexpected error during device manager initialization: {e}")

    def load_devices(self):
        try:
            with open(self.filepath, mode='r', newline='') as file:
                return list(csv.DictReader(file))
        except IOError as e:
            self.logger.log_error(f"Failed to read device file: {e}")
            return []

    def save_device(self, device):
        try:
            with open(self.filepath, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["Key", "Location", "Name", "IP", "Type", "Status"])
                writer.writerow(device)
        except IOError as e:
            self.logger.log_error(f"Failed to save device: {e}")

    def delete_device(self, device_key):
        try:
            devices = self.load_devices()
            devices = [device for device in devices if device['Key'] != device_key]
            with open(self.filepath, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["Key", "Location", "Name", "IP", "Type", "Status"])
                writer.writeheader()
                writer.writerows(devices)
        except IOError as e:
            self.logger.log_error(f"Failed to delete device: {e}")

    def update_device(self, device_key, new_details):
        try:
            devices = self.load_devices()
            updated = False
            for device in devices:
                if device['Key'] == device_key:
                    device.update(new_details)
                    updated = True
            if updated:
                with open(self.filepath, mode='w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=["Key", "Location", "Name", "IP", "Type", "Status"])
                    writer.writeheader()
                    writer.writerows(devices)
        except IOError as e:
            self.logger.log_error(f"Failed to update device: {e}")

class NetworkOperations:
    def __init__(self, config, update_callback, max_queue_size=100):
        self.logger = LogManager.get_instance()
        self.logger.log_debug("Initializing NetworkOperations")
        self.config = config
        self.update_callback = update_callback
        self.task_queue = Queue(maxsize=max_queue_size)  # Set maximum queue size
        self.worker_count = 10  # Increase number of workers if needed
        self.workers = [Thread(target=self.worker) for _ in range(self.worker_count)]
        for worker in self.workers:
            worker.daemon = True
            worker.start()
        self.logger.log_debug("NetworkOperations initialized successfully")

    def worker(self):
        while True:
            try:
                ip = self.task_queue.get(timeout=3)  # Wait for a task or timeout
                if ip is None:  # Check if the worker should shut down
                    self.task_queue.task_done()
                    break
                self.logger.log_info(f"Processing ping for IP: {ip}")
                self._ping(ip)
                self.task_queue.task_done()
            except queue.Empty:
                self.logger.log_error("Worker queue is empty")
                continue

    def ping_device(self, ip):
        try:
            if not self.task_queue.full():
                self.task_queue.put(ip, timeout=1)  # Wait a bit before skipping
                self.logger.log_debug(f"IP {ip} queued for pinging")
            else:
                self.logger.log_info("Queue is full, ping skipped for IP: {}".format(ip))
        except queue.Full:
            self.logger.log_error(f"Failed to queue ping task for IP: {ip} due to full queue")

    def _ping(self, ip):
        attempts = self.config.ping_attempts
        timeout = self.config.ping_timeout
        command = ['ping', '-n', str(attempts), '-w', str(timeout * 1000), ip] if platform.system() == 'Windows' else ['ping', '-c', str(attempts), '-W', str(timeout), ip]
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
            if result.returncode == 0:
                ping_lines = result.stdout.splitlines()
                time_matches = [re.search(r'time=(\d+)ms', line) for line in ping_lines]
                times = [float(match.group(1)) for match in time_matches if match]
                if times:
                    avg_time = sum(times) / len(times)
                    status = f"Online, Avg ping: {avg_time:.2f} ms"
                else:
                    status = "Online, No time reported"
            else:
                status = "Offline, Host Unreachable" if "Destination Host Unreachable" in result.stdout else "Offline, Ping Failed"
        except subprocess.TimeoutExpired:
            self.logger.log_warning(f"Ping timeout for IP: {ip}")
            status = "Offline, Ping Timeout"
        except subprocess.CalledProcessError as e:
            self.logger.log_error(f"Ping process error for IP {ip}: {e}")
            status = "Offline, Error"
        except Exception as e:
            self.logger.log_critical(f"Unexpected error during ping operation for IP {ip}: {e}")
            status = "Offline, Unknown Error"
        self.update_callback(ip, status)

    def stop_workers(self):
        for _ in range(len(self.workers)):
            self.task_queue.put(None)
            self.logger.log_info("Stopping worker threads")

class DeviceDialog(simpledialog.Dialog):
    def __init__(self, master, existing_details=None, action=None):
        self.logger = LogManager.get_instance()
        self.logger.log_debug("Initializing DeviceDialog")
        try:
            self.existing_details = existing_details or {'Key': '', 'Location': '', 'Name': '', 'IP': '', 'Type': '', 'Status': 'Unknown'}
            self.action = action
            super().__init__(master, title="Edit Device Details" if existing_details else "Add Device Details")
            self.logger.log_info("DeviceDialog initialized successfully")
        except Exception as e:
            self.logger.log_error("Failed to initialize DeviceDialog: " + str(e))
            raise e

    def body(self, master):
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

class PingSettingsDialog(simpledialog.Dialog):
    def __init__(self, master, num_attempts, timeout_duration, config_manager):
        self.logger = LogManager.get_instance()
        self.logger.log_debug("Initializing PingSettingsDialog")
        self.num_attempts = num_attempts
        self.timeout_duration = timeout_duration
        self.config_manager = config_manager
        super().__init__(master, title="Ping Settings")
        self.logger.log_info("PingSettingsDialog initialized successfully")

    def body(self, master):
        Label(master, text="Number of Attempts:").grid(row=0, column=0)
        self.num_attempts_var = tk.StringVar(value=str(self.num_attempts))
        self.num_attempts_entry = Entry(master, textvariable=self.num_attempts_var)
        self.num_attempts_entry.grid(row=0, column=1)
        Label(master, text="Timeout Duration (seconds):").grid(row=1, column=0)
        self.timeout_duration_var = tk.StringVar(value=str(self.timeout_duration))
        self.timeout_duration_entry = Entry(master, textvariable=self.timeout_duration_var)
        self.timeout_duration_entry.grid(row=1, column=1)
        return self.num_attempts_entry

    def apply(self):
        num_attempts = int(self.num_attempts_var.get())
        timeout_duration = int(self.timeout_duration_var.get())
        if num_attempts > 10:
            messagebox.showerror("Invalid Input", "Number of attempts cannot exceed 10.")
            self.logger.log_error("Number of attempts cannot exceed 10.")
            return
        self.config_manager.save_settings(num_attempts, timeout_duration)
        self.master.update_refresh_interval()
        self.logger.log_info("Ping settings updated from settings dialog.")

class Application(tk.Frame):
    def __init__(self, master=None):
        self.logger = LogManager.get_instance()
        self.logger.log_debug("Initializing Application")
        super().__init__(master)
        self.master = master
        self.master.title("Python NetMon")
        self.master.state('zoomed')
        self.config_manager = ConfigManager()
        self.device_manager = DeviceManager()
        self.network_ops = NetworkOperations(self.config_manager, self.update_device_status)
        self.update_refresh_interval()
        self.create_menu()
        self.create_widgets()
        self.load_devices()
        self.update_status()
        self.logger.log_debug("Application initialized successfully")

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        edit_menu = tk.Menu(menubar, tearoff=0)
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        menubar.add_cascade(label="Help", menu=help_menu)
        file_menu.add_command(label="Settings", accelerator="Ctrl+S", command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.quit_app)
        edit_menu.add_command(label="Add Device", accelerator="Ctrl+A", command=self.add_device)
        edit_menu.add_command(label="Edit Device", accelerator="Ctrl+E", command=self.edit_device)
        edit_menu.add_command(label="Delete Device", accelerator="Ctrl+D", command=self.delete_device)
        help_menu.add_command(label="Online Help", accelerator="Ctrl+H", command=self.open_online_help)
        help_menu.add_command(label="About", accelerator="Ctrl+I", command=self.show_about)
        self.master.bind("<Control-s>", lambda event: self.open_settings())
        self.master.bind("<Control-q>", lambda event: self.quit_app())
        self.master.bind("<Control-a>", lambda event: self.add_device())
        self.master.bind("<Control-e>", lambda event: self.edit_device())
        self.master.bind("<Control-d>", lambda event: self.delete_device())
        self.master.bind("<Control-h>", lambda event: self.open_online_help())
        self.master.bind("<Control-i>", lambda event: self.show_about())

    def quit_app(self):
        self.master.quit()

    def open_online_help(self):
        webbrowser.open_new_tab(hyperlink)

    def show_about(self):
        messagebox.showinfo("About Python NetMon", f"Python NetMon {version}\nDeveloped by: Chris Collins\nA simple network monitoring tool built with Python and Tkinter.\nFor more information, visit: {hyperlink}")

    def create_widgets(self):
        self.pack(fill='both', expand=True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.tree = ttk.Treeview(self, columns=("Key", "Location", "Name", "IP", "Type", "Status", "Avg Ping"), show="headings")
        for col in ["Key", "Location", "Name", "IP", "Type", "Status", "Avg Ping"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center')
        self.tree.heading("Key", text="Key")
        self.tree.column("Key", width=0, stretch=tk.NO, minwidth=0)
        self.tree.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        style = ttk.Style()
        style.configure("Treeview", font=('Helvetica', 10))
        style.map('Treeview', background=[('selected', 'blue')])
        style.configure("Offline.Treeview")
        style.configure("Pending.Treeview")
        style.configure("Online.Treeview")
        bottom_frame = tk.Frame(self)
        bottom_frame.grid(row=1, column=0, sticky='ew')
        bottom_frame.grid_columnconfigure(1, weight=1)
        self.status_label = tk.Label(bottom_frame, text=f"Next update in {self.countdown} seconds")
        self.status_label.grid(row=0, column=1)
        button_frame = tk.Frame(bottom_frame)
        button_frame.grid(row=1, column=1, pady=10)

    def load_devices(self):
        try:
            self.tree.delete(*self.tree.get_children())
            devices = self.device_manager.load_devices()
            for device in devices:
                tag = "Pending" if device['Status'] == "Pending" else ("Offline" if device['Status'] == "Offline" else "Online")
                self.tree.insert("", "end", values=(device['Key'], device['Location'], device['Name'], device['IP'], device['Type'], device['Status']), tags=(tag,))
            self.sort_devices()
        except Exception as e:
            self.logger.log_error("Failed to load devices: " + str(e))

    def update_refresh_interval(self):
        if self.config_manager.ping_attempts <= 5:
            self.refresh_interval = 60
        elif 5 < self.config_manager.ping_attempts <= 10:
            self.refresh_interval = 90
        self.countdown = self.refresh_interval
        self.logger.log_debug(f"Refresh interval set to {self.refresh_interval} seconds based on ping attempts.")

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        devices = self.device_manager.load_devices()
        for device in devices:
            self.tree.insert("", "end", values=(device['Key'], device['Location'], device['Name'], device['IP'], device['Type'], "Pending", "N/A"), tags=("Pending",))
            self.network_ops.ping_device(device['IP'])
        self.logger.log_debug("Successfully refreshed all devices.")

    def sort_devices(self):
        l = [(self.tree.set(k, "Status"), k) for k in self.tree.get_children('')]
        l.sort(key=lambda t: (t[0] != "Offline", t[0] == "Online"))
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)

    def update_status(self):
        if self.countdown > 0:
            self.status_label.config(text=f"Next update in {self.countdown} seconds")
            self.countdown -= 1
            self.master.after(1000, self.update_status)
        else:
            self.refresh()
            self.countdown = self.refresh_interval
            self.master.after(1000, self.update_status)

    def update_device_status(self, ip, status):
        self.master.after(0, lambda: self._update_device_status(ip, status))

    def _update_device_status(self, ip, status):
        for child in self.tree.get_children():
            values = self.tree.item(child, 'values')
            if values[3] == ip:
                new_values = list(values)
                if ", Avg ping:" in status:
                    status, avg_ping = status.split(", Avg ping:")
                    new_values[5] = status.strip()
                    new_values[6] = avg_ping.strip()
                else:
                    new_values[5] = status
                    new_values[6] = "N/A"
                tag = 'Offline' if "Offline" in status else 'Online' if "Online" in status else 'Pending'
                self.tree.item(child, values=new_values, tags=(tag,))
                self.tree.tag_configure(tag, background='red' if tag == 'Offline' else 'yellow' if tag == 'Pending' else 'white')
        self.sort_devices()

    def open_settings(self):
        try:
            dialog = PingSettingsDialog(self, self.config_manager.ping_attempts, self.config_manager.ping_timeout, self.config_manager)
            if dialog.result:
                self.update_refresh_interval()
        except Exception as e:
            self.logger.log_error("Failed to open settings dialog: " + str(e))

    def add_device(self):
        dialog = DeviceDialog(self.master)
        if dialog.result:
            new_device = dialog.result
            if self.validate_device(new_device):
                new_key = self.device_manager.generate_new_key()
                new_device['Key'] = str(new_key)
                new_device['Status'] = "Pending"
                self.device_manager.save_device(new_device)
                self.refresh()
                messagebox.showinfo("Add Device", "Device successfully added.")
                self.logger.log_info(f"Device added: {new_device}")
            else:
                messagebox.showerror("Add Device", "Failed to add device. Invalid input details.")

    def validate_device(self, device):
        try:
            ipaddress.ip_address(device['IP'])
            return True
        except ValueError:
            self.logger.log_error(f"Invalid IP address: {device['IP']}")
            return False

    def edit_device(self):
        selected_items = self.tree.selection()
        if selected_items:
            item = self.tree.item(selected_items[0], "values")
            existing_details = {
                'Key': item[0],
                'Location': item[1],
                'Name': item[2],
                'IP': item[3],
                'Type': item[4],
                'Status': item[5]
            }
            dialog = DeviceDialog(self.master, existing_details, self.update_device)
            self.logger.log_info(f"Editing device with Key: {existing_details['Key']}")
            if dialog.result:
                self.refresh()

    def update_device(self, new_details):
        device_key = new_details['Key']
        self.device_manager.update_device(device_key, new_details)
        self.refresh()

    def delete_device(self):
        selected_items = self.tree.selection()
        if selected_items:
            item = self.tree.item(selected_items[0], "values")
            device_key = item[0]
            response = messagebox.askyesno("Delete Device", f"Are you sure you want to delete the device with Key {device_key}?")
            if response:
                self.device_manager.delete_device(device_key)
                self.refresh()
                self.logger.log_info(f"Device with Key {device_key} deleted.")
        else:
            messagebox.showinfo("Delete Device", "Please select a device to delete.")

if __name__ == "__main__":
    log_manager = LogManager.get_instance()
    log_manager.log_info("Application started")
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    log_manager.log_info("Application ended")
