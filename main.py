import os
import serial
import threading
import tkinter as tk
from tkinter import Label
import tkinter.ttk as ttk


class SerialMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Serial Monitor - Subvals Boxes")

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
        for i in range(19):  # Increase the range to 19 to match the number of subvals
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
        self.running = True
        self.filename = self.get_new_filename()  # Get a unique filename
        self.serial_thread = threading.Thread(target=self.read_serial_data)
        self.serial_thread.daemon = True
        self.serial_thread.start()
        self.update_gui()

    def get_new_filename(self):
        """Generate a unique filename to prevent overwriting."""
        i = 1
        while True:
            filename = f"file{i}.txt"
            if not os.path.exists(filename):
                return filename
            i += 1

    def write_to_file(self, line):
        """Write a line of serial data to the file."""
        with open(self.filename, "a") as file:
            file.write(line + "\n")  # Write the line of data to the file

    def read_serial_data(self):
        """Read data from the serial port."""
        try:
            with serial.Serial('COM9', 115200, timeout=0.1) as ser:
                while self.running:
                    if ser.in_waiting:
                        line = ser.readline().decode('utf-8', errors='ignore').strip()
                        if line:
                            self.serial_buffer.append(line)
        except serial.SerialException as e:
            self.serial_buffer.append(f"Error: {e}")
        except Exception as e:
            self.serial_buffer.append(f"Unexpected error: {e}")

    def update_gui(self):
        """Update the GUI with new serial data in the correct order."""
        while self.serial_buffer:
            line = self.serial_buffer.pop(0)
            self.raw_data_text.insert(tk.END, line + "\n")
            self.raw_data_text.see(tk.END)  # Scroll to the end

            if line.startswith("$Message length:"):
                value = line.split(":")[1].strip()
                self.box1_value.config(text=value)
            elif line.startswith("Message:"):
                value = line.split(": ", 1)[1].strip()
                try:
                    # Example 'value' format:
                    # [2024/12/19 (Thursday) 13:06:42] accel_x,accel_y,accel_z,...
                    timestamp_part, data_part = value.split("] ", 1)
                    timestamp = timestamp_part.strip("[")
                    subvals = data_part.split(",")

                    # subvals should have 18 values in the corrected format:
                    # 0: accel_x
                    # 1: accel_y
                    # 2: accel_z
                    # 3: gyro_x
                    # 4: gyro_y
                    # 5: gyro_z
                    # 6: imu_temp
                    # 7: bme_temp
                    # 8: bme_pressure
                    # 9: bme_altitude
                    # 10: bme_humidity
                    # 11: gps_fix
                    # 12: gps_fix_quality
                    # 13: gps_lat
                    # 14: gps_lon
                    # 15: gps_speed
                    # 16: gps_altitude
                    # 17: gps_satellites

                    # Update the timestamp (index 0 in self.subval_values)
                    self.subval_values[0].config(text=timestamp.strip())

                    # Update each of the subvals
                    for i in range(len(subvals)):
                        self.subval_values[i+1].config(text=subvals[i].strip())

                except ValueError:
                    print("Error parsing telemetry data:", value)
            elif line.startswith("RSSI:"):
                value = line.split(":")[1].strip()
                self.box3_value.config(text=value)
            elif line.startswith("Snr:"):
                value = line.split(":")[1].strip()
                self.box4_value.config(text=value)

            self.write_to_file(line)

        self.root.after(10, self.update_gui)

    def quit(self):
        """Handle cleanup when quitting the application."""
        self.running = False
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SerialMonitorApp(root)
    root.mainloop()
