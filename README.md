Parts:
- Raspberry Pi Pico W series (e.g. pico W, pico 2W). Board must support Wi-Fi
- Breadboard or ability to solder to the Pico
- Single color LED light
- 100 Ohm resistor (220 will likely also work fine)
- Reed switch
- A box with a lift that can lift to separate parts of the reed switch. I used this one from Amazon:

Code assumes you have a settings.toml file on your CIRCUITPY board with the following parameters set to your Wi-Fi Network Name & Password:
CIRCUITPY_WIFI_SSID="Wi-Fi Network Name Here"
CIRCUITPY_WIFI_PASSWORD="Wi-Fi Password Here"

Required CircuitPython libraries (CircUp will install all of these):
- circuitpython_schedule.mpy (from the community bundle)
- adafruit_datetime.mpy
- adafruit_ntp.mpy
