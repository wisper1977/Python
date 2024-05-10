# Python NetMon - 1.1.1.1

Welcome to the Python NetMon repository! Python NetMon is a simple, intuitive network monitoring tool built with Python and Tkinter. It allows users to manage network devices, monitor their status, and view detailed ping statistics in real-time.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Version History](#version-history)
- [Future Plans](#future-plans)
- [Contributing](#contributing)
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
   git clone https://github.com/wisper1977/Python/tree/a3544690fe81d7580825c59a1b9e0a7137ccabeb/Python%20NetMon

2. Navigate to the project directory:
   ```bash
   cd Python\ NetMon\ 1.1.0

No additional installation required if you have Python installed.

## Usage
To run the application, navigate to the directory containing the script and run:

   python netmon.py

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

## Keyboard Shortcuts

The application supports several keyboard shortcuts to make navigation and operations faster and more convenient:

- **Ctrl + N**: Open the dialog to add a new device.
- **Ctrl + E**: Edit the selected device.
- **Ctrl + D**: Delete the selected device.
- **Ctrl + S**: Open settings.
- **F1**: Open online help or documentation.

Make sure a device is selected in the main window for edit or delete shortcuts to work.

## Version History

### v1.1.1.1 - Current Version
**Release Date:** TBD
Security Enhancements:
- Minor Bug Fixes
- Enhanced logging

### v1.1.1 - GUI Update
**Release Date:** May 8, 2024
Security Enhancements:
- Added input validation to prevent common security vulnerabilities.
- Implemented more robust error handling throughout the network operations.
- Added keyboard shortcuts for improved navigation and usability.
- Improved logging for network operations and error handling.
- Fixed UI bugs related to device management dialogs.

### v1.1.0 - Major Update
**Release Date:** April 20, 2024
Major Improvements:
- Introduced the device editing and deleting functionality.
- Added validation for IP addresses when adding or editing devices.
- Enhanced performance for device status updates.
- Redesigned the entire user interface for a more modern look.
- Introduced a multi-threaded approach for handling network operations.
- Added a logging system with file output for troubleshooting.

### v1.0.4 - Additional Features
**Release Date:** April 5, 2024
New Features:
- Implemented device editing and deletion capabilities.
- Added support for saving device configurations.

### v1.0.3 - User Interface Improvements
**Release Date:** March 20, 2024
UI Updates:
- Enhanced user interface with better layout and navigation.
- Added color coding to status indicators for devices.

### v1.0.2 - Performance Enhancements
**Release Date:** March 15, 2024
- Fixed a bug in the network pinging process where timeouts were not handled correctly.
- Updated UI responsiveness during network scans.
- Optimized the network ping process for faster response times.
- Reduced CPU usage during idle periods.

### v1.0.1 - Bug Fixes
**Release Date:** February 25, 2024
- Minor bug fixes in the configuration management.
- Improved error messages for easier troubleshooting.
- Fixed an issue where ping results were not updating correctly.
- Minor UI adjustments for better readability.

### v1.0.0 - Initial Release
**Release Date:** February 10, 2024
- Features Introduced:
- Basic network monitoring capabilities.
- Ping devices manually to check connectivity.
- Display results in a simple user interface.

## Future Plans
- Log Rotation and Archiving: Ensure logs are rotated and archived properly to avoid consuming too much disk space, which might already be handled but could be enhanced with compression or more complex retention policies.
- Detailed Device Views: Allow users to click on a device in the list to view more detailed information or statistics in a separate dialog or pane.
- Input Validation: Rigorously validate all inputs, especially those that could affect network operations or subprocess invocations, to prevent injection attacks.
- Notification System: Implement notifications or alerts based on device status changes or failures detected during monitoring.

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/wisper1977/Python/blob/main/Python%20NetMon/License.md) file for details.
