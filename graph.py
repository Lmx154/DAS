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

def get_trajectory_and_altitude_fig(time_data, lat_data, lon_data, alt_data):
    """
    Create a figure with two subplots:
    1) A 2D trajectory (lat vs. lon)
    2) An altitude vs. time line plot
    """
    fig = plt.Figure(figsize=(10, 4), dpi=100)

    # -- Subplot 1: ground track (lon vs. lat) --
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.plot(lon_data, lat_data, marker='o', linestyle='-')
    ax1.set_xlabel('Longitude (°)')
    ax1.set_ylabel('Latitude (°)')
    ax1.set_title('Rocket Ground Track')
    ax1.grid(True)

    # -- Subplot 2: altitude vs. time --
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.plot(time_data, alt_data, color='blue')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Altitude (m)')
    ax2.set_title('Altitude vs. Time')
    ax2.grid(True)

    fig.tight_layout()  # To reduce overlap
    return fig


# Add other plots as needed, e.g. get_altitude_fig(), get_gyro_fig(), etc.
