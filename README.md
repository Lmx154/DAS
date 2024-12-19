# DAS

Data Acquisition System.

## Installation

To install the dependencies for this project, run the following command:

```sh
pip install -r requirements.txt
```

# Simulated Hardware
# Telemetry Data Summary Table
```bash
[2000/01/01 (Saturday) 00:08:58] 15.19,0.1,0.42,87.71,-54.22,71.53,-56.5,-69.7,0.0,838206.0,0,1,2,32.9394,-106.922,77.95,838206.0,8
RSSI: -99
Snr: 8.32
```

| Data String Value | Source Code (C)                     | Description                                   |
|--------------------|--------------------------------------|-----------------------------------------------|
| `2000/01/01`       | `rtc.now()`                        | RTC timestamp.                               |
| `15.19`            | `accel.getAccelX_mss()`            | X-axis acceleration (m/s²).                  |
| `0.1`              | `accel.getAccelY_mss()`            | Y-axis acceleration (m/s²).                  |
| `0.42`             | `accel.getAccelZ_mss()`            | Z-axis acceleration (m/s²).                  |
| `87.71`            | `gx`                               | X-axis gyroscope (degrees/s).                |
| `-54.22`           | `gy`                               | Y-axis gyroscope (degrees/s).                |
| `71.53`            | `gz`                               | Z-axis gyroscope (degrees/s).                |
| `-56.5`            | `accel.getTemperature_C()`         | IMU temperature (Celsius).                   |
| `0.0`              | `bme.readPressure()`               | Atmospheric pressure (bar).                  |
| `838206.0`         | `bme.readAltitude()`               | Altitude (meters).                           |
| `32.9394`          | `ddmmToDD(GPS.latitude)`           | GPS latitude (decimal degrees).              |
| `-106.922`         | `ddmmToDD(GPS.longitude)`          | GPS longitude (decimal degrees).             |
| `77.95`            | `GPS.speed`                        | GPS speed (km/h).                            |
| `8`                | `GPS.satellites`                   | Number of satellites.                        |
| `-99`              | `LoRa.packetRssi()`                | Signal strength (dBm).                       |
| `8.32`             | `LoRa.packetSnr()`                 | Signal-to-noise ratio.                       |


# Actual Hardware

# Table Mapping Data String Values to Variables

```bash
$Message length: 138
Message: [2024/5/18 (Saturday) 21:50:56] 0.08,-0.40,-9.74,14.00,16.00,-96.00,31.25,33.56,1009.91,-31.06,35.39,1,2,26.273800,-98.431976,0.16,68.00,8
RSSI: -99
Snr: 8.00
```



### Actual Hardware Table

| Value in Data String | Mapped Variable   | Description                                   |
|----------------------|-------------------|-----------------------------------------------|
| `0.08`               | `accel_x`         | IMU X-axis acceleration (m/s²)                |
| `-0.40`              | `accel_y`         | IMU Y-axis acceleration (m/s²)                |
| `-9.74`              | `accel_z`         | IMU Z-axis acceleration (m/s²)                |
| `14.00`              | `gyro_x`          | IMU X-axis angular velocity (°/s)             |
| `16.00`              | `gyro_y`          | IMU Y-axis angular velocity (°/s)             |
| `-96.00`             | `gyro_z`          | IMU Z-axis angular velocity (°/s)             |
| `31.25`              | `imu_temp`        | IMU internal temperature (°C)                 |
| `33.56`              | `bme_temp`        | BME280 temperature reading (°C)               |
| `1009.91`            | `bme_pressure`    | BME280 atmospheric pressure (hPa)             |
| `-31.06`             | `bme_altitude`    | BME280 altitude (m)                           |
| `35.39`              | `bme_humidity`    | BME280 humidity (%)                           |
| `1`                  | `gps_fix`         | GPS fix status (1 = fixed, 0 = not fixed)      |
| `2`                  | `gps_fix_quality` | GPS fix quality (e.g., 1 = GPS fix, 2 = DGPS) |
| `26.273800`          | `gps_lat`         | GPS latitude (decimal degrees)                 |
| `-98.431976`         | `gps_lon`         | GPS longitude (decimal degrees)                |
| `0.16`               | `gps_speed`       | GPS ground speed (m/s)                        |
| `68.00`              | `gps_altitude`    | GPS altitude (m)                              |
| `8`                  | `gps_satellites`  | Number of GPS satellites in use               |

---

### Rewritten Data String with Abbreviations

```bash
[timestamp] accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, imu_temp, bme_temp, bme_pressure, bme_altitude, bme_humidity, gps_fix, gps_fix_quality, gps_lat, gps_lon, gps_speed, gps_altitude, gps_satellites
```