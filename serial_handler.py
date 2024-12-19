# serial_handler.py

import serial
import threading
import os
from utils import get_new_filename

class SerialHandler:
    def __init__(self, app):
        self.app = app
        self.serial_buffer = []
        self.running = False
        self.serial_thread = None
        self.filename = get_new_filename()

    def start_reading(self):
        """Start the serial reading thread."""
        if not self.serial_thread or not self.serial_thread.is_alive():
            self.running = True
            self.serial_thread = threading.Thread(target=self.read_serial_data, daemon=True)
            self.serial_thread.start()

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

    def write_to_file(self, line):
        """Write a line of serial data to the file."""
        with open(self.filename, "a") as file:
            file.write(line + "\n")  # Write the line of data to the file

    def open_serial(self):
        """Open the serial port by starting the reading thread."""
        self.start_reading()

    def close_serial(self):
        """Close the serial port by stopping the reading thread."""
        self.running = False
        if self.serial_thread:
            self.serial_thread.join(timeout=1)
