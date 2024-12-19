# DAS

Data Acquisition System.

## Installation

To install the dependencies for this project, run the following command:

```sh
pip install -r requirements.txt
```


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

