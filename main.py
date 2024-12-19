import os
import serial
import threading
import tkinter as tk
from tkinter import Label


class SerialMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Serial Monitor - Subvals Boxes")

        # GUI Elements for Message Length, RSSI, Snr
        self.box1_label = Label(root, text="Message Length:", font=("Arial", 14))
        self.box1_value = Label(root, text="N/A", font=("Arial", 14), bg="white", width=40, anchor="w")
        self.box3_label = Label(root, text="RSSI:", font=("Arial", 14))
        self.box3_value = Label(root, text="N/A", font=("Arial", 14), bg="white", width=40, anchor="w")
        self.box4_label = Label(root, text="Snr:", font=("Arial", 14))
        self.box4_value = Label(root, text="N/A", font=("Arial", 14), bg="white", width=40, anchor="w")

        # Place Message Length, RSSI, Snr boxes
        self.box1_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.box1_value.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.box3_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.box3_value.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.box4_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.box4_value.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Boxes for subvals (11 values)
        self.subval_labels = ["AccelerometerX", "AccelerometerY", "AccelerometerZ", "GyroX", "GyroY", "GyroZ",
                              "Temp1", "Temp2", "Pressure", "Orientation1", "Orientation2"]
        self.subval_values = []
        for i in range(11):
            label = Label(root, text=self.subval_labels[i], font=("Arial", 14))
            value = Label(root, text="N/A", font=("Arial", 14), bg="white", width=40, anchor="w")
            label.grid(row=3+i, column=0, padx=10, pady=5, sticky="e")
            value.grid(row=3+i, column=1, padx=10, pady=5, sticky="w")
            self.subval_values.append(value)

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
                    for i in range(min(len(subvals), 11)):  # Ensure we only update the 11 boxes
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
