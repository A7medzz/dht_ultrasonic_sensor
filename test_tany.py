import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def get_distance():
    return random.uniform(10, 400)  # Simulate distance in centimeters

def get_temperature():
    return random.uniform(0, 100)   # Simulate temperature in Celsius

def get_humidity():
    return random.uniform(0, 60)    # Simulate humidity in percentage

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

start_time = time.time()

# Create a figure with 3 subplots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8))

try:
    with open("sensor_log.txt", "a") as file:
        def data_collection(frame):
            timestamp = time.time() - start_time
            distance = get_distance()
            temperature = get_temperature()
            humidity = get_humidity()

            print(f"Time: {timestamp:.2f}s - Distance: {distance:.2f} cm, Temperature: {temperature:.2f} C, Humidity: {humidity:.2f}%")
            file.write(f"time:{timestamp:.2f}\n----------\n\t{distance:.2f}\n\t{temperature:.2f}\n\t{humidity:.2f}\n---------\n")
            file.flush()

            timestamps.append(timestamp)
            distances.append(distance)
            temperatures.append(temperature)
            humidities.append(humidity)
            
            # Update the plot with the new data
            update_plot(frame, timestamps, distances, temperatures, humidities, ax1, ax2, ax3)


            time.sleep(5)

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
