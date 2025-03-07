import network
import time
import BlynkLib
from machine import Pin
from neopixel import NeoPixel

# Wi-Fi Credentials
WIFI_SSID = "Sweet home"
WIFI_PASS = "Ahmad456"

# Blynk Auth Token
BLYNK_AUTH = "y6ZzeVPywJDNXc0shr7weejGlmVZ0wBz"
#define BLYNK_TEMPLATE_ID "TMPL6CZak3dP7"
#define BLYNK_TEMPLATE_NAME "RGB"
#define BLYNK_AUTH_TOKEN "JBDzE9SUyIf8vO-Ft7NgRJ5QkR6Eq5QY"
# Built-in RGB LED on GPIO 48
RGB_PIN = 48
NUM_LEDS = 1  # Only one built-in LED
rgb_led = NeoPixel(Pin(RGB_PIN, Pin.OUT), NUM_LEDS)

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)

    while not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        time.sleep(1)

    print("Connected to Wi-Fi:", wlan.ifconfig())

connect_wifi()

# Initialize Blynk
# Initialize Blynk without SSL
blynk = BlynkLib.Blynk(BLYNK_AUTH)




# Function to control RGB LED
def set_color(r, g, b):
    rgb_led[0] = (r, g, b)
    rgb_led.write()

# Blynk Button Handlers
@blynk.on("V0")  # Button for Red
def v0_write(value):
    if int(value[0]) == 1:
        set_color(255, 0, 0)  # Red ON
    else:
        set_color(0, 0, 0)  # OFF

@blynk.on("V1")  # Button for Green
def v1_write(value):
    if int(value[0]) == 1:
        set_color(0, 255, 0)  # Green ON
    else:
        set_color(0, 0, 0)  # OFF

@blynk.on("V2")  # Button for Blue
def v2_write(value):
    if int(value[0]) == 1:
        set_color(0, 0, 255)  # Blue ON
    else:
        set_color(0, 0, 0)  # OFF

# Main Loop
while True:
    blynk.run()