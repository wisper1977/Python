# Description: This module contains the ApplicationGUI class that creates the main GUI for the application.

import os
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from modules.device_manager import DeviceManager
from modules.log_manager import LogManager
from modules.log_viewer_gui import LogViewerGUI
from modules.device_dialog import DeviceDialog
from modules.ping_settings_dialog import PingSettingsDialog

class ApplicationGUI:
    def __init__(self, master, app):
        """Initialize the GUI with a reference to the main application and device manager."""
        self.logger = LogManager.get_instance()
        self.master = master
        self.app = app  # Reference to the main application class to access business logic
        self.log_viewer = LogViewerGUI(master, app)  # Initialize the log viewer window
        self.device_manager = DeviceManager()
        self.version = "1.1.3.1"
        self.hyperlink = "https://tinyurl.com/PyNetMon"
        self.developer = "Chris Collins"
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
            
            # Check the operating system
            if os.name == 'nt':  # If the OS is Windows
                self.master.iconbitmap('media/NetMon.ico')
            else:  # For other OSs, you can use a .png or .gif file
                icon = tk.PhotoImage(file='media/NetMon.png')
                self.master.iconphoto(False, icon)
            
            self.tree.grid(sticky='nsew', padx=10, pady=10)
            self.master.grid_rowconfigure(0, weight=1)
        
            self.tree.bind("<Double-1>", self.on_double_click)

            # Timer label
            self.timer_label = tk.Label(self.master, text="")
            self.timer_label.grid(sticky='ew', padx=10, pady=10)
            self.master.grid_rowconfigure(1, weight=0)
            self.master.grid_columnconfigure(0, weight=1)
        except Exception as e:
            print(f"Error creating widgets: {e}")
            
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
            webbrowser.open_new_tab(self.hyperlink)
        except Exception as e:
            self.logger.log_error("Failed to open online help: " + str(e))
            raise e

    def show_about(self):
        """Display the 'About' dialog with information about the application."""
        try:
            messagebox.showinfo("About Python NetMon", f"Version: {self.version}\nDeveloped by: {self.developer}\nA simple network monitoring tool built with Python and Tkinter.")
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
