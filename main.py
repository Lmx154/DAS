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

        # Boxes for subvals (15 values)
        self.subval_labels = [
            "RTC Timestamp",          # `2000/01/01`
            "X-axis Acceleration",    # `15.19`
            "Y-axis Acceleration",    # `0.1`
            "Z-axis Acceleration",    # `0.42`
            "X-axis Gyroscope",       # `87.71`
            "Y-axis Gyroscope",       # `-54.22`
            "Z-axis Gyroscope",       # `71.53`
            "IMU Temperature",        # `-56.5`
            "Atmospheric Pressure",   # `0.0`
            "Altitude",               # `838206.0`
            "GPS Latitude",           # `32.9394`
            "GPS Longitude",          # `-106.922`
            "GPS Speed",              # `77.95`
            "Number of Satellites",   # `8`
            "Signal Strength"         # `-99`
        ]
        self.subval_values = []
        for i in range(15):
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

    def write_to_file(self):
        """Write the current values to the file in columns."""
        with open(self.filename, "a") as file:
            # Collect data for all boxes
            row_data = [
                self.box1_value.cget("text"),  # Message Length
                *[box.cget("text") for box in self.subval_values],  # Subvals
                self.box3_value.cget("text"),  # RSSI
                self.box4_value.cget("text")   # Snr
            ]
            # Write as a single row
            file.write("\t".join(row_data) + "\n")

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
        """Update the GUI with new serial data."""
        while self.serial_buffer:
            line = self.serial_buffer.pop(0)
            self.raw_data_text.insert(tk.END, line + "\n")
            self.raw_data_text.see(tk.END)  # Scroll to the end

            if line.startswith("$Message length:"):
                value = line.split(":")[1].strip()
                self.box1_value.config(text=value)
            elif line.startswith("Message:"):
                value = line.split(": ")[1].strip()
                try:
                    # Parse subvals
                    _, subvals = value.split("] ", 1)
                    subvals = subvals.split(",")

                    # Update each subval box
                    for i in range(min(len(subvals), 15)):  # Ensure we only update the 15 boxes
                        self.subval_values[i].config(text=subvals[i].strip())
                except ValueError:
                    print("Error parsing subvals:", value)
            elif line.startswith("RSSI:"):
                value = line.split(":")[1].strip()
                self.box3_value.config(text=value)
            elif line.startswith("Snr:"):
                value = line.split(":")[1].strip()
                self.box4_value.config(text=value)

        # Write to the file after updating the GUI
        self.write_to_file()

        self.root.after(10, self.update_gui)

    def quit(self):
        """Handle cleanup when quitting the application."""
        self.running = False
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SerialMonitorApp(root)
    root.mainloop()
