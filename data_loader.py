# data_loader.py

import numpy as np

def load_acceleration_data_from_file(file_path):
    time_list = []
    accel_x_list = []
    accel_y_list = []
    accel_z_list = []

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith("Message:"):
                # Example: "Message:[2000/01/02(Sunday)00:41:57]15.22, -0.40, -9.74"
                # Remove the prefix
                line = line[len("Message:"):]  # " [2000/01/02(Sunday)00:41:57]15.22, -0.40, -9.74"

                # Now split on "]"
                if "]" in line:
                    # left part = "[2000/01/02(Sunday)00:41:57"
                    # right part = "15.22, -0.40, -9.74"
                    timestamp_part, numeric_part = line.split("]", 1)
                    numeric_part = numeric_part.strip()
                    
                    # Now split on commas
                    parts = numeric_part.split(',')
                    if len(parts) < 3:
                        # Not enough data
                        continue

                    try:
                        # We don't necessarily have a "time" float, but let's say we treat the first numeric as 'time'
                        # or we skip 'time' if you want to store that "timestamp_part" as a string.
                        ax_val = float(parts[0].strip())
                        ay_val = float(parts[1].strip())
                        az_val = float(parts[2].strip())

                        # Maybe you store the timestamp as 0 or a placeholder
                        t_val = 0.0  # or parse from 'timestamp_part' if needed

                        time_list.append(t_val)
                        accel_x_list.append(ax_val)
                        accel_y_list.append(ay_val)
                        accel_z_list.append(az_val)

                    except ValueError:
                        # Not numeric
                        continue

                continue  # done with this line

            else:
                # If it's not a "Message:" line, maybe it *is* in "time, ax, ay, az" format
                parts = line.split(',')
                if len(parts) < 4:
                    continue
                try:
                    t_val = float(parts[0].strip())
                    ax_val = float(parts[1].strip())
                    ay_val = float(parts[2].strip())
                    az_val = float(parts[3].strip())
                    time_list.append(t_val)
                    accel_x_list.append(ax_val)
                    accel_y_list.append(ay_val)
                    accel_z_list.append(az_val)
                except ValueError:
                    # can't parse
                    continue

    # Convert to NumPy arrays (optional)
    import numpy as np
    time_data = np.array(time_list)
    accel_x = np.array(accel_x_list)
    accel_y = np.array(accel_y_list)
    accel_z = np.array(accel_z_list)

    return time_data, accel_x, accel_y, accel_z

