import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from gpiozero import DistanceSensor
import adafruit_dht
import board

# Setup sensor GPIO pins and types
TRIG_PIN = 23  # GPIO pin connected to TRIG of the ultrasonic sensor
ECHO_PIN = 24  # GPIO pin connected to ECHO of the ultrasonic sensor
DHT_PIN = board.D20  # Using board.D4 for GPIO4 on the Raspberry Pi

# Initialize the DHT sensor using the Adafruit library
dht_sensor = adafruit_dht.DHT11(DHT_PIN)

# Initialize the ultrasonic sensor
ultrasonic = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN)
start_time = time.time()

# Functions to get actual sensor readings
def get_distance():
    return ultrasonic.distance * 100  # Convert to cm

def get_temperature_and_humidity():
    try:
        temperature = dht_sensor.temperature
        humidity = dht_sensor.humidity
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        temperature, humidity = None, None
        print(f"Error reading DHT22 sensor: {error}")
    return temperature, humidity

# Function to update plots
def update_plot(frame, timestamps, distances, temperatures, humidities, ax1, ax2, ax3):
    ax1.clear()
    ax1.plot(timestamps, distances, label="Distance (cm)")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Distance (cm)")
    ax1.set_title("Distance Over Time")
    ax1.legend()
    
    ax2.clear()
    ax2.plot(timestamps, temperatures, label="Temperature (°C)", color='orange')
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Temperature (°C)")
    ax2.set_title("Temperature Over Time")
    ax2.legend()
    
    ax3.clear()
    ax3.plot(timestamps, humidities, label="Humidity (%)", color='green')
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("Humidity (%)")
    ax3.set_title("Humidity Over Time")
    ax3.legend()
    
    plt.tight_layout()

timestamps = []
distances = []
temperatures = []
humidities = []

# Create a figure with 3 subplots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8))

try:
    with open("Rpi_sensor_log.txt", "a") as file:
        def data_collection(frame):
            timestamp = time.time() - start_time
            distance = get_distance()
            temperature, humidity = get_temperature_and_humidity()

            if temperature is not None and humidity is not None:
                print(f"Time: {timestamp:.2f}s - Distance: {distance:.2f} cm, Temperature: {temperature:.2f} °C, Humidity: {humidity:.2f}%")
                file.write(f"time: {timestamp:.2f}\n")
                file.write(f"Distance: {distance:.2f} cm\n")
                file.write(f"Temperature: {temperature:.2f} °C\n")
                file.write(f"Humidity: {humidity:.2f} %\n")
                file.write("---------\n")
                file.flush()

                timestamps.append(timestamp)
                distances.append(distance)
                temperatures.append(temperature)
                humidities.append(humidity)
                
                # Update the plot with the new data
                update_plot(frame, timestamps, distances, temperatures, humidities, ax1, ax2, ax3)

            time.sleep(1)

        ani = animation.FuncAnimation(
            fig, 
            data_collection, 
            frames=100,  # Number of frames corresponds to the number of data points
            interval=1000,
            repeat=False
        )

        plt.show()

except KeyboardInterrupt:
    print("Data collection interrupted.")
