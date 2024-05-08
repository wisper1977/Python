import configparser, csv, subprocess, platform, ipaddress, logging, threading, queue, re
import tkinter as tk
from queue import Queue, Empty
from threading import Thread
from pathlib import Path
from tkinter import ttk, simpledialog, Label, Entry, messagebox
from logging.handlers import RotatingFileHandler

# Set up logging directories
log_directory = Path('log')
log_directory.mkdir(exist_ok=True)  # Create the log directory if it does not exist

# Set up logging configuration
logging.basicConfig(
    level=logging.DEBUG,  # Capture all levels of logging
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_directory / 'log_file.txt'),  # File handler for output
        logging.StreamHandler()  # Console handler for output
    ]
)

class ConfigManager:
    def __init__(self, config_path='config/config.ini'):
        self.config_path = Path(config_path)
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        if not self.config_path.exists():
            self.config['PING'] = {'Attempts': '3', 'Timeout': '100'}
            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)
            logging.debug("No config file found. Created a new one with default settings.")
        else:
            self.config.read(self.config_path)
            logging.debug("Config file loaded successfully.")
        self.ping_attempts = self.config.getint('PING', 'Attempts')
        self.ping_timeout = self.config.getint('PING', 'Timeout')

    def save_settings(self, attempts, timeout):
        if attempts > 10:
            logging.error("Attempt to set ping attempts greater than 10. Limiting to 10.")
            attempts = 10
        self.config.set('PING', 'Attempts', str(attempts))
        self.config.set('PING', 'Timeout', str(timeout))
        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)
        logging.debug(f"Settings saved: Attempts={attempts}, Timeout={timeout}")
        self.load_config()

class DeviceManager:
    def __init__(self, filepath='config/equipment.csv'):
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            with open(self.filepath, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["Key", "Location", "Name", "IP", "Type", "Status"])
                writer.writeheader()

    def load_devices(self):
        with open(self.filepath, mode='r', newline='') as file:
            return list(csv.DictReader(file))

    def generate_new_key(self):
        with open(self.filepath, mode='r', newline='') as file:
            max_key = max((int(row['Key']) for row in csv.DictReader(file)), default=0)
        return max_key + 1

    def save_device(self, device):
        with open(self.filepath, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["Key", "Location", "Name", "IP", "Type", "Status"])
            writer.writerow(device)

    def delete_device(self, device_key):
        devices = self.load_devices()
        devices = [device for device in devices if device['Key'] != device_key]
        with open(self.filepath, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["Key", "Location", "Name", "IP", "Type", "Status"])
            writer.writeheader()
            writer.writerows(devices)

    def update_device(self, device_key, new_details):
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

class NetworkOperations:
    def __init__(self, config, update_callback, max_queue_size=100):
        self.config = config
        self.update_callback = update_callback
        self.task_queue = Queue(maxsize=max_queue_size)  # Set maximum queue size
        self.worker_count = 10  # Increase number of workers if needed
        self.workers = [Thread(target=self.worker) for _ in range(self.worker_count)]
        for worker in self.workers:
            worker.daemon = True
            worker.start()

    def worker(self):
        while True:
            try:
                ip = self.task_queue.get(timeout=3)  # Wait for a task or timeout
                if ip is None:  # Check if the worker should shut down
                    self.task_queue.task_done()
                    break
                logging.debug(f"Processing ping for IP: {ip}")
                self._ping(ip)
                self.task_queue.task_done()
            except queue.Empty:
                continue

    def ping_device(self, ip):
        try:
            if not self.task_queue.full():
                self.task_queue.put(ip, timeout=1)  # Wait a bit before skipping
                logging.debug(f"IP {ip} queued for pinging")
            else:
                logging.warning("Queue is full, skipping ping for IP: {}".format(ip))
        except queue.Full:
            logging.error("Failed to queue ping task for IP: {} due to full queue".format(ip))

    def _ping(self, ip):
        logging.debug(f"Starting ping for IP: {ip}")
        attempts = self.config.ping_attempts
        timeout = self.config.ping_timeout
        command = ['ping', '-n', str(attempts), '-w', str(timeout * 1000), ip] if platform.system() == 'Windows' else ['ping', '-c', str(attempts), '-W', str(timeout), ip]
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
            logging.debug(f"Ping completed for IP {ip}: STDOUT: {result.stdout} STDERR: {result.stderr}")
            if result.returncode == 0:
                # Handle successful ping
                ping_lines = result.stdout.splitlines()
                time_matches = [re.search(r'time=(\d+)ms', line) for line in ping_lines]
                times = [float(match.group(1)) for match in time_matches if match]
                if times:
                    avg_time = sum(times) / len(times)
                    status = f"Online, Avg ping: {avg_time:.2f} ms"
                else:
                    status = "Online, No time reported"
            else:
                # Handle failed ping
                if "100% loss" in result.stdout or "Destination Host Unreachable" in result.stdout:
                    status = "Offline, Host Unreachable"
                else:
                    status = "Offline, Ping Failed"
        except subprocess.TimeoutExpired:
            logging.error(f"Ping request for IP {ip} timed out")
            status = "Offline, Ping Timeout"
        except Exception as e:
            logging.error(f"An error occurred while pinging IP {ip}: {str(e)}")
            status = "Offline, Error"

        self.update_callback(ip, status)

    def stop_workers(self):
        for _ in range(len(self.workers)):
            self.task_queue.put(None)

class DeviceDialog(simpledialog.Dialog):
    def __init__(self, master, existing_details=None, action=None):
        try:
            self.existing_details = existing_details or {'Key': '', 'Location': '', 'Name': '', 'IP': '', 'Type': '', 'Status': 'Unknown'}
            self.action = action
            super().__init__(master, title="Edit Device Details" if existing_details else "Add Device Details")
        except Exception as e:
            logging.error("Failed to initialize DeviceDialog", exc_info=True)
            raise e

    def body(self, master):
        try:
            # Creating labels for each field
            Label(master, text="Key:").grid(row=0, column=0)
            Label(master, text="Location:").grid(row=1, column=0)
            Label(master, text="Name:").grid(row=2, column=0)
            Label(master, text="IP:").grid(row=3, column=0)
            Label(master, text="Type:").grid(row=4, column=0)

            # Initialize entry variables using values from existing_details if available
            self.key_var = tk.StringVar(master, self.existing_details['Key'])
            self.location_var = tk.StringVar(master, self.existing_details['Location'])
            self.name_var = tk.StringVar(master, self.existing_details['Name'])
            self.ip_var = tk.StringVar(master, self.existing_details['IP'])
            self.type_var = tk.StringVar(master, self.existing_details['Type'])

            # Create Entry widgets for each field
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

            return key_entry  # Return the Entry widget that should get the initial focus
        except Exception as e:
            logging.error("Failed to create body for DeviceDialog", exc_info=True)
            raise e

    def apply(self):
        try:
            details = {
                'Key': self.key_var.get(),
                'Location': self.location_var.get(),
                'Name': self.name_var.get(),
                'IP': self.ip_var.get(),
                'Type': self.type_var.get(),
                'Status': 'Unknown'  # Default status for new device, edit does not change status here
            }
            if self.action:
                self.action(details)
            self.result = details
        except Exception as e:
            logging.error("Failed to apply changes in DeviceDialog", exc_info=True)
            raise e

class PingSettingsDialog(simpledialog.Dialog):
    def __init__(self, master, num_attempts, timeout_duration, config_manager):
        # Initialize attributes before calling the parent constructor which eventually calls `body`.
        self.num_attempts = num_attempts
        self.timeout_duration = timeout_duration
        self.config_manager = config_manager
        super().__init__(master, title="Ping Settings")

    def body(self, master):
        # Create and place widgets in the dialog; `self.num_attempts` and `self.timeout_duration` are already set.
        Label(master, text="Number of Attempts:").grid(row=0, column=0)
        self.num_attempts_var = tk.StringVar(value=str(self.num_attempts))
        self.num_attempts_entry = Entry(master, textvariable=self.num_attempts_var)
        self.num_attempts_entry.grid(row=0, column=1)

        Label(master, text="Timeout Duration (seconds):").grid(row=1, column=0)
        self.timeout_duration_var = tk.StringVar(value=str(self.timeout_duration))
        self.timeout_duration_entry = Entry(master, textvariable=self.timeout_duration_var)
        self.timeout_duration_entry.grid(row=1, column=1)

        return self.num_attempts_entry  # Setting initial focus to the num_attempts_entry widget

    def apply(self):
        num_attempts = int(self.num_attempts_var.get())
        timeout_duration = int(self.timeout_duration_var.get())
        if num_attempts > 10:
            messagebox.showerror("Invalid Input", "Number of attempts cannot exceed 10.")
            return
        self.config_manager.save_settings(num_attempts, timeout_duration)
        self.master.update_refresh_interval()  # Update the main application's refresh interval
        logging.debug("Ping settings updated from settings dialog.")

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Python NetMon")  # Set the title of the main window
        self.master.state('zoomed')  # This maximizes the Tkinter window.
        
        self.config_manager = ConfigManager()
        self.device_manager = DeviceManager()
        self.network_ops = NetworkOperations(self.config_manager, self.update_device_status)
        self.update_refresh_interval()
        
        self.create_menu()
        self.create_widgets()
        self.load_devices()  # Load devices immediately but delay the ping
        self.update_status()

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        edit_menu = tk.Menu(menubar, tearoff=0)
        
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # Adding 'Settings' under 'File'
        file_menu.add_command(label="Settings", command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        
        # Adding Device management options under 'Edit'
        edit_menu.add_command(label="Add Device", command=self.add_device)
        edit_menu.add_command(label="Edit Device", command=self.edit_device)
        edit_menu.add_command(label="Delete Device", command=self.delete_device)

    def create_widgets(self):
        # Configure the layout
        self.pack(fill='both', expand=True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Set up the treeview with an additional column for Average Ping
        self.tree = ttk.Treeview(self, columns=("Key", "Location", "Name", "IP", "Type", "Status", "Avg Ping"), show="headings")
        for col in ["Key", "Location", "Name", "IP", "Type", "Status", "Avg Ping"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center')
            
        # Configuring the column widths can be optional, add if needed:
        # self.tree.column("Location", width=100)
        # self.tree.column("Name", width=120)
        # self.tree.column("IP", width=100)
        # self.tree.column("Type", width=100)
        # self.tree.column("Status", width=150)
        # self.tree.column("Avg Ping", width=120)
        
        # Hide the 'Key' column while still using it in the background
        self.tree.heading("Key", text="Key")
        self.tree.column("Key", width=0, stretch=tk.NO, minwidth=0)  # Set width and stretch to minimize and hide the column

        self.tree.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        # Define the styles for different device statuses
        style = ttk.Style()
        style.configure("Treeview", font=('Helvetica', 10))  # Default font size and family
        style.map('Treeview', background=[('selected', 'blue')])

        # These styles are applied based on tags that you will assign when inserting items
        style.configure("Offline.Treeview", background="red", foreground="white")
        style.configure("Pending.Treeview", background="yellow", foreground="black")
        style.configure("Online.Treeview", background="white", foreground="black")

        # Status label and buttons at the bottom
        bottom_frame = tk.Frame(self)
        bottom_frame.grid(row=1, column=0, sticky='ew')
        bottom_frame.grid_columnconfigure(1, weight=1)  # Center the button frame

        self.status_label = tk.Label(bottom_frame, text=f"Next update in {self.countdown} seconds")
        self.status_label.grid(row=0, column=1)  # Status label is at the top of the buttons

        button_frame = tk.Frame(bottom_frame)
        button_frame.grid(row=1, column=1, pady=10)  # Button frame below the status label

    def load_devices(self):
        try:
            self.tree.delete(*self.tree.get_children())
            devices = self.device_manager.load_devices()
            for device in devices:
                tag = "Pending" if device['Status'] == "Pending" else ("Offline" if device['Status'] == "Offline" else "Online")
                self.tree.insert("", "end", values=(device['Key'], device['Location'], device['Name'], device['IP'], device['Type'], device['Status']), tags=(tag,))
            self.sort_devices()
        except Exception as e:
            logging.error("Failed to load devices", exc_info=True)

    def update_refresh_interval(self):
        if self.config_manager.ping_attempts <= 5:
            self.refresh_interval = 60
        elif 5 < self.config_manager.ping_attempts <= 10:
            self.refresh_interval = 90
        self.countdown = self.refresh_interval  # Reset the countdown whenever the interval changes
        logging.debug(f"Refresh interval set to {self.refresh_interval} seconds based on ping attempts.")

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        devices = self.device_manager.load_devices()
        for device in devices:
            self.tree.insert("", "end", values=(device['Key'], device['Location'], device['Name'], device['IP'], device['Type'], "Pending", "N/A"), tags=("Pending",))
            self.network_ops.ping_device(device['IP'])
        logging.info("Successfully refreshed all devices.")

    def sort_devices(self):
        """ Sort devices in the treeview based on status priority: Offline, Pending, Online. """
        l = [(self.tree.set(k, "Status"), k) for k in self.tree.get_children('')]
        l.sort(key=lambda t: (t[0] != "Offline", t[0] == "Online"))
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)

    def update_status(self):
        """Update the status label and refresh the device statuses periodically."""
        if self.countdown > 0:
            self.status_label.config(text=f"Next update in {self.countdown} seconds")
            self.countdown -= 1
            self.master.after(1000, self.update_status)
        else:
            self.refresh()
            self.countdown = self.refresh_interval
            self.master.after(1000, self.update_status)

    def update_device_status(self, ip, status):
        """ Update the device status in the Treeview. """
        self.master.after(0, lambda: self._update_device_status(ip, status))

    def _update_device_status(self, ip, status):
        logging.debug(f"Updating status for IP {ip} to {status}")
        for child in self.tree.get_children():
            values = self.tree.item(child, 'values')
            if values[3] == ip:  # Assuming IP is at index 3
                new_values = list(values)
                if ", Avg ping:" in status:
                    status, avg_ping = status.split(", Avg ping:")
                    new_values[5] = status.strip()  # Status
                    new_values[6] = avg_ping.strip()  # Avg Ping
                else:
                    new_values[5] = status  # Status without ping time
                    new_values[6] = "N/A"  # No Avg Ping data
                tag = 'Offline' if "Offline" in status else 'Online' if "Online" in status else 'Pending'
                self.tree.item(child, values=new_values, tags=(tag,))
                self.tree.tag_configure(tag, background='red' if tag == 'Offline' else 'yellow' if tag == 'Pending' else 'white')
        self.sort_devices()

    def open_settings(self):
        try:
            dialog = PingSettingsDialog(self, self.config_manager.ping_attempts, self.config_manager.ping_timeout, self.config_manager)
            if dialog.result:  # You might need to adjust this depending on the dialog result handling
                self.update_refresh_interval()
        except Exception as e:
            logging.error("Failed to open settings dialog", exc_info=True)

    def add_device(self):
        dialog = DeviceDialog(self.master)
        if dialog.result:
            new_device = dialog.result
            if self.validate_device(new_device):
                new_key = self.device_manager.generate_new_key()
                new_device['Key'] = str(new_key)
                new_device['Status'] = "Pending"  # New devices start as Pending
                self.device_manager.save_device(new_device)
                self.refresh()
                messagebox.showinfo("Add Device", "Device successfully added.")
            else:
                messagebox.showerror("Add Device", "Failed to add device. Invalid input details.")

    def validate_device(self, device):
        try:
            ipaddress.ip_address(device['IP'])
            return True
        except ValueError:
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
            if dialog.result:
                self.refresh()

    def update_device(self, new_details):
        device_key = new_details['Key']
        self.device_manager.update_device(device_key, new_details)
        self.refresh()

    def delete_device(self):
        selected_items = self.tree.selection()
        if selected_items:
            item = this.tree.item(selected_items[0], "values")
            device_key = item[0]
            response = messagebox.askyesno("Delete Device", f"Are you sure you want to delete the device with Key {device_key}?")
            if response:
                self.device_manager.delete_device(device_key)
                self.refresh()
        else:
            messagebox.showinfo("Delete Device", "Please select a device to delete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
