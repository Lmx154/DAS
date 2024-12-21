# graph.py

import matplotlib
matplotlib.use("TkAgg")  # Use the Tkinter backend
import matplotlib.pyplot as plt

def get_acceleration_time_fig(time_data, accel_x, accel_y, accel_z):
    """
    Create and return a Matplotlib Figure (no plt.show())
    with acceleration data vs. time.
    """
    fig = plt.Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(time_data, accel_x, label='accel_x (m/s²)')
    ax.plot(time_data, accel_y, label='accel_y (m/s²)')
    ax.plot(time_data, accel_z, label='accel_z (m/s²)')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Acceleration (m/s²)')
    ax.set_title('Acceleration vs. Time')
    ax.legend()
    ax.grid(True)
    return fig

# Add other plots as needed, e.g. get_altitude_fig(), get_gyro_fig(), etc.
