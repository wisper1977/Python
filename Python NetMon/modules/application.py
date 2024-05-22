# Version: 1.1.3.1
# Description: Module to manage the main application window and setup the GUI.

import csv, os, threading, pygame, logging
import tkinter as tk
from modules.device_manager import DeviceManager
from modules.application_gui import ApplicationGUI
from modules.log_manager import LogManager
from modules.network_operations import NetworkOperations
from pathlib import Path
from logging.handlers import RotatingFileHandler

class Application(tk.Frame):
    def __init__(self, master=None, config_manager=None, log_manager=None):
        """Initialize the main application with the root window and setup the GUI."""
        try:
            super().__init__(master)
            self.master = master
            self.master.title("Python NetMon")
            self.master.state('zoomed')
            
            self.config_manager = config_manager
            self.logger = log_manager
            self.setup_logging()
            self.device_manager = DeviceManager(filepath='config/equipment.csv')
            self.gui = ApplicationGUI(master, self)
            self.network_ops = NetworkOperations(config=self.config_manager, update_callback=self.update_callback)

            self.gui.load_devices()
            self.gui.initiate_refresh_cycle()
        except Exception as e:
            self.logger.log_error("Failed to initialize application: " + str(e))
            raise e
   
    def setup_logging(self):
        """Setup logging configuration for the application."""
        try:
            log_directory = Path(self.config_manager.get_setting('Logging', 'log_directory', 'log'))
            log_directory.mkdir(exist_ok=True)
            log_file = self.config_manager.get_setting('Logging', 'log_file', 'log_file.txt')
            log_file_path = log_directory / log_file
            archive_directory = Path(self.config_manager.get_setting('Logging', 'archive_directory', 'log/archive'))
            archive_directory.mkdir(parents=True, exist_ok=True)
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5),
                    logging.StreamHandler()
                ]
            )
        except Exception as e:
            self.log_manager.log_error(f"Error setting up logging: {e}")
            raise e

    def update_callback(self, ip, message):
        """Callback method for network operations updates."""
        try:
            self.update_device_status(ip, message)
        except Exception as e:
            self.logger.log_error("Failed to update device status: " + str(e))
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
                            def play_sound():
                                pygame.mixer.init()
                                sound = pygame.mixer.Sound(os.path.join('media', 'alert.wav'))  # Create a Sound object
                                for _ in range(3):
                                    sound.play()  # Play the sound using the Sound object
                                    pygame.time.wait(int(sound.get_length() * 1000))  # Get the length of the sound using the Sound object

                            threading.Thread(target=play_sound).start()

                        # Update status in CSV
                        data = []
                        with open(os.path.join('config', 'equipment.csv'), 'r') as file:
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
                        with open(os.path.join('config', 'equipment.csv'), 'w', newline='') as file:
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