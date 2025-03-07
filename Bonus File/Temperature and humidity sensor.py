import network
import BlynkLib
from machine import Pin, I2C, Timer
import machine
import ssd1306
import dht
import time

# WiFi Credentials
WIFI_SSID = "Sweet home"     
WIFI_PASS = "Ahmad456"  

# Blynk Auth Token 
BLYNK_AUTH = "zb4B5Ef_t_FqQxfOV2yKwFtzHaeE4VLV"

# Connect to WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASS)

# Wait for connection with timeout
timeout = 10  # 10 seconds timeout
while not wifi.isconnected() and timeout > 0:
    time.sleep(1)
    timeout -= 1

if wifi.isconnected():
    print("Connected to WiFi")
else:
    print("Failed to connect to WiFi")

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

DHT_PIN = 4  # DHT11 data pin
button = Pin(0, Pin.IN, Pin.PULL_UP)
dht_sensor = dht.DHT11(machine.Pin(DHT_PIN))  # Initialize DHT11 sensor

# Initialize OLED display
i2c = machine.I2C(scl=machine.Pin(9), sda=machine.Pin(8))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

oled_on = True  # Track OLED state

def toggle_oled(pin):
    global oled_on
    time.sleep_ms(200)  # Debounce delay
    if not pin.value():  # Ensure button press is detected
        oled_on = not oled_on
        if oled_on:
            oled.poweron()
        else:
            oled.poweroff()

# Attach the interrupt to the button's falling edge
button.irq(trigger=Pin.IRQ_FALLING, handler=toggle_oled)

# Main loop
while True:
    try:
        dht_sensor.measure()
        time.sleep(2)  # Ensure enough delay for accurate readings
        temp = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        
        # Validate the sensor readings
        if temp is None or humidity is None:
            print("Sensor reading failed, retrying...")
            continue
        if temp < 0 or temp > 50 or humidity < 20 or humidity > 90:
            print(f"Unrealistic values detected! Temp: {temp}, Humidity: {humidity}. Retrying...")
            continue
        
        print(f"Temp: {temp}°C, Humidity: {humidity}%")

        # Send data to Blynk
        blynk.virtual_write(0, temp)  # V0 for temperature
        blynk.virtual_write(1, humidity)  # V1 for humidity
        
        # Display on OLED if it's on
        if oled_on:
            oled.fill(0)
            oled.text(f"Temp: {temp} C", 0, 0)
            oled.text(f"Humidity: {humidity}%", 0, 16)
            oled.text("XD", 36, 48)  # Just smile :)
            oled.show()
    
    except Exception as e:
        print("Error reading DHT11 sensor:", e)

    blynk.run()
    time.sleep(2)  # Increased delay to improve accuracy
