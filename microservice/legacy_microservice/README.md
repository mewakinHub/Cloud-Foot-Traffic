# Bag Detection System

This project is designed to detect and track bags on a conveyor belt using YOLOv8 for object detection and an IOU-based tracker for tracking. The system is currently configured to handle one bag at a time, ensuring accurate tracking and counting of bags.

## Table of Contents

- [System Requirements](#system-requirements)
- [Operational Guidelines](#Operational-Guidelines)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [Developer Guide: Startup Automation](#developer-guide-startup-automation)
- [Troubleshooting](#troubleshooting)

## System Requirements

- **Operating System**: Windows 10/11 (for `.bat` scripts), Linux (manual setup)
- **GPU**: NVIDIA GPU with CUDA 12.1 or higher
- **Python**: 3.9+
- **Conda**: Latest version

## Operational Guidelines 
**Single Bag Detection:** The system currently supports detecting and tracking only one bag at a time. To ensure accurate detection and tracking:

- **Camera Setup**: Position your camera so that only one bag is visible in the frame at any given time. Avoid placing two bags too close together on the conveyor belt.
- **Bag Spacing**: Ensure that bags enter the frame one by one. If two bags appear too close to each other, the system may not function correctly, leading to inaccurate results.

**Conveyor Belt Speed:** The speed of the conveyor belt must match the speed used in the test video provided in the bucket. This synchronization is critical for maintaining the system's accuracy.

**Handling Conveyor Delays**: If a bag gets stuck on the conveyor belt, it is recommended to stop the software immediately. This prevents errors and ensures the system remains in sync with the physical setup.

**Model Compatibility:** If you change the model's weight file (best.pt), ensure that the model’s class names align with the type_bag configuration. Mismatches can cause the system to fail in identifying and processing bags correctly.

## Setup Instructions

### Why Use a Conda Environment?

The application relies on a Conda environment named **`bag-detection`** for all its dependencies. This specific environment is crucial because the `.bat` scripts are designed to work exclusively within it. Without this environment, the application will not function correctly.

### Setup Steps

1. **Clone the Repository (or manually install from zip file)**: 

   ```bash
   git clone https://github.com/yourusername/bag-detection.git
   cd bag-detection
   ```

2. **Create Conda Environment**:

   ```bash
   conda create --name bag-detection python=3.9
   ```

3. **Activate Conda Environment**: (For Non-Windows users)

   ```bash
   conda activate bag-detection
   ```

4. **Install CUDA Toolkit**

   - **Purpose**: Required for running PyTorch models with GPU acceleration.
   - **Download**: Obtain the installer from the [Nvidia official website](https://developer.nvidia.com/cuda-toolkit).
   - **Verify Installation**:
     ```bash
     nvcc --version  # Should output: CUDA version: V12.2.140
     nvidia-smi      # Should output: Driver Version: 560.70
     ```

5. **Run Setup Script (Windows Only)**:

   Execute the `setup.bat` file to install all necessary dependencies:
   NOTE: you can done by clicking icon on file explorer!
   ```batch
   setup.bat
   ```

   > **Note:** If you encounter timeouts during installation, rerun the script until all dependencies are successfully installed. Once set up, the application will run instantly.

   > **Note:** The setup script is designed for Windows users only. Linux users must install dependencies manually.

6. **Configure RTSP URL:**

   - Modify the RTSP URL in `configs/client_config.yaml` to your CCTV camera's IP address.

7. **Place Trained Model**:

   - Place your trained `best.pt` model in the `assets/models/` directory.

## Running the Application

1. **Activate Conda Environment**: (For Non-Windows users)

   ```bash
   conda activate bag-detection
   ```

2. **Run the Application (Windows Only)**:

   Execute the `run.bat` file to start the application:

   ```batch
   run.bat
   ```

3. **Stop the Application**:

   Press **q** during runtime to attempt to stop the application. 
   **Note**: It might require more than one press to close the program completely. After pressing 'q' once, allow the script to run to completion to ensure that output files are written correctly.

   - **Important**: If 'q' is pressed prematurely or the program doesn't close properly, restart the application to avoid any issues with incomplete outputs.


## Developer Guide: Startup Automation (Optional)

To automate the application startup on Windows, create a shortcut for `run.bat` and place it in the startup folder:

1. Press `Windows + R`, type `shell:startup`, and press `OK`.
2. Copy the shortcut into this folder to ensure the application starts automatically on system boot.

## Troubleshooting

1. **Conda Environment Not Found**:
   - Ensure the Conda environment is named **`bag-detection`**.
   - Verify that the environment is activated before running any scripts.

2. **Pressing 'q' Does Not Stop the Application**:
   - If pressing 'q' once does not stop the application, press it again and wait.
   - Do not exit abruptly, as this might prevent output from being saved properly.

3. **Display Issues**:
   - If the CV display remains active after stopping, manually close it and restart the application.


## Developer Guide

For developers looking to modify or scale this project, here are some additional details:

### 1. **Tracking and Interval Results**

- **IOU Tracker Capabilities**: The `provider.iou_tracker` can track multiple bags simultaneously, organizing them by unique `id`, `bdbox`, `age`, and `updated` status. However, the current interval result system is designed to process only one bag at a time. When a new bag enters the frame, the interval result is reset, and previous data is cleared. 

- **Scaling Up**: If you want to scale this project to handle multiple bags simultaneously:
  - **Enhance the Interval Result System**: Modify the interval result system to collect and process results that match each tracked bag's `id` or another unique key. This change would allow the system to track and process multiple bags independently, using the tracking information stored in the IOU tracker.