# gui.py

import tkinter as tk
from tkinter import Label
import tkinter.ttk as ttk
from serial_handler import SerialHandler
from utils import get_new_filename

class SerialMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Serial Monitor - Subvals Boxes")

        # Initialize Serial Handler
        self.serial_handler = SerialHandler(self)

        # Create a menu bar
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Add Serial menu
        self.serial_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Serial", menu=self.serial_menu)
        self.serial_menu.add_command(label="Open Serial", command=self.open_serial)
        self.serial_menu.add_command(label="Close Serial", command=self.close_serial)

        # Add File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Exit", command=self.quit)

        # Add Options menu
        self.options_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Options", menu=self.options_menu)

        # Add Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About")

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=1, fill="both")

        # Create a frame for data
        self.data_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.data_frame, text="Data")

        # GUI Elements for Message Length, RSSI, Snr
        self.box1_label = Label(self.data_frame, text="Message Length:", font=("Arial", 14))
        self.box1_value = Label(self.data_frame, text="N/A", font=("Arial", 14), bg="white", width=40, anchor="w")
        self.box3_label = Label(self.data_frame, text="RSSI:", font=("Arial", 14))
        self.box3_value = Label(self.data_frame, text="N/A", font=("Arial", 14), bg="white", width=40, anchor="w")
        self.box4_label = Label(self.data_frame, text="Snr:", font=("Arial", 14))
        self.box4_value = Label(self.data_frame, text="N/A", font=("Arial", 14), bg="white", width=40, anchor="w")

        # Place Message Length, RSSI, Snr boxes
        self.box1_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.box1_value.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.box3_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.box3_value.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.box4_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.box4_value.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Labels for subvals
        self.subval_labels = [
            "RTC Timestamp",
            "X-axis Acceleration (accel_x)",
            "Y-axis Acceleration (accel_y)",
            "Z-axis Acceleration (accel_z)",
            "X-axis Gyroscope (gyro_x)",
            "Y-axis Gyroscope (gyro_y)",
            "Z-axis Gyroscope (gyro_z)",
            "IMU Temperature (imu_temp)",
            "BME Temp (bme_temp)",
            "BME Pressure (bme_pressure)",
            "BME Altitude (bme_altitude)",
            "BME Humidity (bme_humidity)",
            "GPS Fix (gps_fix)",
            "GPS Fix Quality (gps_fix_quality)",
            "GPS Latitude (gps_lat)",
            "GPS Longitude (gps_lon)",
            "GPS Speed (gps_speed)",
            "GPS Altitude (gps_altitude)",
            "GPS Satellites (gps_satellites)"
        ]

        self.subval_values = []
        for i in range(len(self.subval_labels)):
            label = Label(self.data_frame, text=self.subval_labels[i], font=("Arial", 14))
            value = Label(self.data_frame, text="N/A", font=("Arial", 14), bg="white", width=40, anchor="w")
            label.grid(row=3+i, column=0, padx=10, pady=5, sticky="e")
            value.grid(row=3+i, column=1, padx=10, pady=5, sticky="w")
            self.subval_values.append(value)

        # Create a text widget for raw data at the bottom
        self.raw_data_text = tk.Text(root, wrap="word", height=10, width=80)
        self.raw_data_text.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.X)

        # Serial Communication Variables
        self.serial_buffer = []
        self.filename = get_new_filename()  # Get a unique filename
        self.serial_handler.start_reading()

        self.update_gui()

    def update_gui(self):
        """Update the GUI with new serial data in the correct order."""
        while self.serial_handler.serial_buffer:
            line = self.serial_handler.serial_buffer.pop(0)
            self.raw_data_text.insert(tk.END, line + "\n")
            self.raw_data_text.see(tk.END)  # Scroll to the end

            if line.startswith("$Message length:"):
                value = line.split(":", 1)[1].strip()
                self.box1_value.config(text=value)
            elif line.startswith("Message:"):
                value = line.split(": ", 1)[1].strip()
                try:
                    # Example 'value' format:
                    # [2024/12/19 (Thursday) 13:06:42] accel_x,accel_y,accel_z,...
                    timestamp_part, data_part = value.split("] ", 1)
                    timestamp = timestamp_part.strip("[")
                    subvals = data_part.split(",")

                    # Update the timestamp (index 0 in self.subval_values)
                    if len(self.subval_values) > 0:
                        self.subval_values[0].config(text=timestamp.strip())

                    # Update each of the subvals
                    for i in range(len(subvals)):
                        if i+1 < len(self.subval_values):
                            self.subval_values[i+1].config(text=subvals[i].strip())

                except ValueError:
                    print("Error parsing telemetry data:", value)
            elif line.startswith("RSSI:"):
                value = line.split(":", 1)[1].strip()
                self.box3_value.config(text=value)
            elif line.startswith("Snr:"):
                value = line.split(":", 1)[1].strip()
                self.box4_value.config(text=value)

            self.serial_handler.write_to_file(line)

        self.root.after(10, self.update_gui)

    def open_serial(self):
        """Open the serial port."""
        self.serial_handler.open_serial()

    def close_serial(self):
        """Close the serial port."""
        self.serial_handler.close_serial()

    def quit(self):
        """Handle cleanup when quitting the application."""
        self.serial_handler.close_serial()
        self.root.destroy()
