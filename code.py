# Medications Reminder Box
import board, os, socketpool, wifi, adafruit_ntp, rtc, time, digitalio
import circuitpython_schedule as schedule

# alarm times should be strings in 24 hrs time
# e.g. 00:00 is midnight, 12:00 is noon, 11:59 pm is 23:59
# alarm_times = ["05:00"]
alarm_times = ["18:08"]

# set up the LED
led = digitalio.DigitalInOut(board.GP0)
led.switch_to_output()
led.value = True
# Flash LED when program is first run_pending
flash = True

# set up door sensor / magnetic switch
door_sensor = digitalio.DigitalInOut(board.GP16)
door_sensor.switch_to_input(pull=digitalio.Pull.UP)

# Get wifi AP credentials from settings.toml file
wifi_ssid = os.getenv("CIRCUITPY_WIFI_SSID")
wifi_password = os.getenv("CIRCUITPY_WIFI_PASSWORD")

if wifi_ssid is None:
   print("WiFi credentials are kept in settings.toml, please add them there!")
   raise ValueError("SSID not found in environment variables") # force quit

# Connect to WiFi
print(f"Trying to connect to: {wifi_ssid}")
try:
   wifi.radio.connect(wifi_ssid, wifi_password)
   print(f"Connected to {wifi_ssid} Wi-Fi!")
except (ConnectionError, TypeError) as e:
   print(f"Failed to connect: {e}")
   raise # force quit

# Create socket pool for network operations
pool = socketpool.SocketPool(wifi.radio)

# Get the time
# after connected to Wi-Fi and pool is created - setup the clock
clock = rtc.RTC()
ntp = adafruit_ntp.NTP(pool, tz_offset=-4)  # -5 for Eastern Time (EST)
# default will update the time every 3600 seconds, meaning once an hour.
# Note: For daylight saving time adjustment, you would need to change tz_offset manually
# EST is UTC-5, EDT is UTC-4

def get_time():
    try:
        # Get time from NTP server
        current_time = ntp.datetime
        print(f"{current_time}")
        # format & print time & date
        printable_time = f"{current_time.tm_hour:d}:{current_time.tm_min:02d}:{current_time.tm_sec:02d}"
        printable_date = f"{current_time.tm_mon:d}/{current_time.tm_mday:d}/{current_time.tm_year:02d}"
        print(f"printable_time {printable_time}")
        print(f"printable_date {printable_date}")
        # Update the RTC
        clock.datetime = current_time
    except Exception as e:
        print("Error getting NTP time:\n", str(e))

def job():
    led.value = True # turn on the light
    print("Time to take your meds!")

# Call get_time() once, first, to get the time from the Internet
get_time()

# Schedule the jobs
for alarm_time in alarm_times: # go through all alarm time strings
    schedule.every().day.at(alarm_time).do(job)
    print(f"scheduled alarm at: {alarm_time}")

schedule.every().day.at("00:00").do(get_time) # update time at midnight each day

print("Running Medications Reminder Box...")
while True:
    if flash:
        led.value = not led.value
        time.sleep(0.5)
        if door_sensor.value: # when door is opened
            print(" - STOP FLASH!! - ")
            led.value = False # turn off LED
            flash = False # and stop flashing
    else: # light isn't flashing, so light is steady at any alarm_times
        schedule.run_pending() # check scheduled jobs
        if door_sensor.value: # door opened
            led.value = False
        else: # door closed
            pass
    time.sleep(0.2)

