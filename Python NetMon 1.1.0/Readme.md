# Python NetMon

Welcome to the Python NetMon repository! Python NetMon is a simple, intuitive network monitoring tool built with Python and Tkinter. It allows users to manage network devices, monitor their status, and view detailed ping statistics in real-time.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Contributing](#contributing)
- [Support](#support)
- [License](#license)

## Features

- **Device Management**: Add, edit, and delete network devices.
- **Real-Time Monitoring**: Continuously ping devices to monitor their status.
- **User Interface**: Simple and clean GUI for easy operation.
- **Logging**: Detailed logging of application activities and errors.
- **Keyboard Shortcuts**: Quick access to common actions using keyboard shortcuts.

## Requirements

- Python 3.x
- Tkinter (typically included with Python)
- Additional Python libraries: `csv`, `configparser`, `subprocess`, `platform`, `ipaddress`, `logging`, `threading`, `queue`, `re`, `webbrowser`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/wisper1977/Python/tree/main/Python%20NetMon%201.1.0

2. Navigate to the project directory:
   ```bash
   cd Python\ NetMon\ 1.1.0

No additional installation required if you have Python installed.

## Usage
To run the application, navigate to the directory containing the script and run:

   ```bash
   python netmon1.1.1.py

## Adding a New Device

To add a new device to the network monitoring list, follow these steps:

1. Open the application.
2. Navigate to `Edit > Add Device` from the menu bar.
3. A dialog box will appear prompting you to enter the device details:
   - **Key**: A unique identifier for the device (usually managed by the system).
   - **Location**: The physical or logical location of the device.
   - **Name**: A descriptive name for the device.
   - **IP**: The IP address of the device.
   - **Type**: The type of device (e.g., router, switch, server).
4. After filling out all the fields, click "OK" to add the device to the list.
5. The device will now appear in the main window with a status of "Pending" until the next refresh, when its status will update based on its response to ping requests.

## Editing a Device

To edit an existing device's details:

1. Select the device you want to edit from the list in the main window.
2. Navigate to `Edit > Edit Device` from the menu bar.
3. The same dialog box used for adding a device will appear, with the fields pre-populated with the device's current details.
4. Change the details as needed:
   - You can modify the Location, Name, IP, and Type fields.
5. Once you've made the necessary changes, click "OK" to update the device's details.
6. The modified details will reflect immediately in the device list.

## Deleting a Device

To remove a device from the monitoring list:

1. Select the device you wish to delete from the list in the main window.
2. Navigate to `Edit > Delete Device` from the menu bar.
3. A confirmation dialog will appear asking if you are sure about removing the device.
4. Click "Yes" to remove the device permanently.
5. The device will be removed from the list and will no longer be monitored.
