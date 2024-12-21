# gui.py

import tkinter as tk
from tkinter import Label, filedialog, messagebox
import tkinter.ttk as ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import graph
import data_loader
from serial_handler import SerialHandler
from utils import get_new_filename
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog, messagebox

class SerialMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DAS GUI")

        # ---------------- MENU BAR ----------------
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Serial menu
        self.serial_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Serial", menu=self.serial_menu)

        # Initialize Serial Handler
        self.serial_handler = SerialHandler(self)

        # Add commands to the Serial menu
        self.serial_menu.add_command(label="Open Serial", command=self.open_serial)
        self.serial_menu.add_command(label="Close Serial", command=self.close_serial)
        self.serial_menu.add_command(label="Select Serial", command=self.select_serial)
        
        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Replay Data", command=self.replay_data)
        self.file_menu.add_command(label="Load Data File for Accel", command=self.load_accel_data)
        self.file_menu.add_command(label="Load Trajectory & Altitude File", command=self.load_trajectory_altitude_data)
        self.file_menu.add_command(label="Close Loaded Graph", command=self.close_accel_data)
        self.file_menu.add_command(label="Exit", command=self.quit)

        # Options menu
        self.options_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Options", menu=self.options_menu)

        # Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)

        # ---------------- NOTEBOOK / TABS ----------------
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=1, fill="both")

        self.data_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.data_frame, text="Data")

        self.visualization_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.visualization_frame, text="Data Visualization")

        # Remove the buttons from the visualization tab
        # self.load_data_button = tk.Button(
        #     self.visualization_frame,
        #     text="Load Data File for Accel",
        #     command=self.load_accel_data
        # )
        # self.load_data_button.pack(side=tk.LEFT, pady=10, padx=5)

        # self.close_data_button = tk.Button(
        #     self.visualization_frame,
        #     text="Close Data",
        #     command=self.close_accel_data
        # )
        # self.close_data_button.pack(side=tk.LEFT, pady=10, padx=5)

        # ---------------- SUBVAL LABELS/VALUES ----------------
        self.subval_labels = [
            "RTC Timestamp",              # index 0
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
        for i, label_text in enumerate(self.subval_labels):
            label = Label(self.data_frame, text=label_text, font=("Arial", 14))
            value = Label(self.data_frame, text="N/A", font=("Arial", 14), bg="white", width=40, anchor="w")
            label.grid(row=3+i, column=0, padx=10, pady=5, sticky="e")
            value.grid(row=3+i, column=1, padx=10, pady=5, sticky="w")
            self.subval_values.append(value)

        # ---------------- RAW DATA TEXT BOX ----------------
        self.raw_data_text = tk.Text(root, wrap="word", height=10, width=80)
        self.raw_data_text.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.X)

        # ---------------- SERIAL & GUI LOOP SETUP ----------------
        self.serial_buffer = []
        self.filename = get_new_filename()
        self.serial_handler.start_reading()

        self.update_gui()

    # ---------------- MISSING METHODS ADDED ----------------
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

    def replay_data(self):
        """Replay data from a selected file."""
        # For example:
        file_path = filedialog.askopenfilename(
            title="Select Replay Data File",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
        if not file_path:
            return
        self.serial_handler.replay_data(file_path)
        messagebox.showinfo("Replay", f"Replaying data from {file_path}")

    def show_about(self):
        """Display the About dialog."""
        messagebox.showinfo("About", "DAS GUI\nVersion 1.0\nDeveloped by Red Rocket inc.")

    def load_trajectory_altitude_data(self):
        """Prompt user for a file containing time, lat, lon, alt, then show the trajectory & altitude plot."""
        file_path = filedialog.askopenfilename(
            title="Select Trajectory & Altitude File",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
        if not file_path:
            return  # user cancelled

        try:
            # 1) Load data
            time_data, lat_data, lon_data, alt_data = (
                data_loader.load_trajectory_altitude_data_from_file(file_path)
            )

            # 2) Create figure
            fig = graph.get_trajectory_and_altitude_fig(
                time_data, lat_data, lon_data, alt_data
            )

            # 3) Embed in the visualization_frame
            self.traj_alt_canvas = FigureCanvasTkAgg(fig, master=self.visualization_frame)
            self.traj_alt_canvas.draw()
            self.traj_alt_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Data Error", str(e))

    def load_accel_data(self):
        """
        Load acceleration data from file & show in the visualization frame.
        """
        file_path = filedialog.askopenfilename(
            title="Select Data File",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
        if not file_path:
            return

        try:
            time_data, accel_x, accel_y, accel_z = data_loader.load_acceleration_data_from_file(file_path)
            fig = graph.get_acceleration_time_fig(time_data, accel_x, accel_y, accel_z)

            self.canvas = FigureCanvasTkAgg(fig, master=self.visualization_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Data Error", str(e))

    def close_accel_data(self):
        """
        Close the loaded acceleration data visualization.
        """
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().pack_forget()
            del self.canvas

    def select_serial(self):
        """List available serial ports and show them to the user."""
        ports = self.serial_handler.list_serial_ports()
        ports_str = "\n".join(ports) if ports else "No serial ports found."
        messagebox.showinfo("Available Serial Ports", ports_str)

    def update_gui(self):
        """
        Continuously read from self.serial_handler.serial_buffer and update
        subvals + raw_data_text in the GUI. Then schedule another call.
        """
        while self.serial_handler.serial_buffer:
            line = self.serial_handler.serial_buffer.pop(0)
            self.raw_data_text.insert(tk.END, line + "\n")
            self.raw_data_text.see(tk.END)

            # Example parsing logic for your subvals:
            if line.startswith("$Message length:"):
                pass
            elif line.startswith("Message:"):
                # e.g. "Message: [2024/12/19 ... ] accel_x,accel_y,accel_z,..."
                value = line.split(": ", 1)[1].strip()
                try:
                    timestamp_part, data_part = value.split("] ", 1)
                    timestamp = timestamp_part.strip("[")
                    subvals = data_part.split(",")

                    # subval_values[0] is the timestamp
                    if len(self.subval_values) > 0:
                        self.subval_values[0].config(text=timestamp.strip())

                    for i, subv in enumerate(subvals):
                        if i+1 < len(self.subval_values):
                            self.subval_values[i+1].config(text=subv.strip())
                except ValueError:
                    messagebox.showerror("Parsing Error", f"Error parsing: {value}")

            elif line.startswith("RSSI:"):
                pass
            elif line.startswith("Snr:"):
                pass

            self.serial_handler.write_to_file(line)

        # Schedule next update
        self.root.after(10, self.update_gui)
