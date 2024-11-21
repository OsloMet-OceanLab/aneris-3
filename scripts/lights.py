"""
author: @rambech
"""

import gpiod as GPIO
from time import sleep
from numpy import around
from datetime import datetime, timedelta
from suntime import Sun
from pytz import timezone
from lib import utils
from scripts import configuration
from apscheduler.schedulers.background import BackgroundScheduler

# Setup PWM pin
PWM_pin = 12
chip = GPIO.Chip('gpiochip4')
led_line = chip.get_line(PWM_pin)

PWM_FREQUENCY = 100          # Hertz
PWM_PERIOD = 1/PWM_FREQUENCY  # Seconds
MAX_PERIOD = 1900 * 1e-6     # 1900 microseconds
MIN_PERIOD = 1100 * 1e-6     # 1100 microseconds
time_format = "%H:%M"

def sunset_sunrise() -> tuple[datetime, datetime]:
    """
    Returns a tuple of sunset and sunrise of Vilanova la Geltrú in CET
    """

    # Fetch suntime in Vilanova i la Geltrú
    sun = Sun(41.2152, 1.7274)
    cet = timezone("CET")

    # The night goes from sunset to sunrise
    sunset = utils.roundHalfHour(sun.get_sunset_time(time_zone=cet))
    sunrise = utils.roundHalfHour(sun.get_sunrise_time(time_zone=cet))

    # TODO: Remove this
    # sunset = datetime(2024, 11, 21, 9, 30)
    # sunrise = datetime(2024, 11, 21, 11, 0)

    return sunset, sunrise

def on():
    try:
        # Request gpio service to give access
        led_line.request(consumer="LED", type=GPIO.LINE_REQ_DIR_OUT)
        led_line.set_value(1)
    finally:
        # Always release after setting pin value
        led_line.release()


def off():
    try:
        # Request gpio service to give access
        led_line.request(consumer="LED", type=GPIO.LINE_REQ_DIR_OUT)
        led_line.set_value(0)
    finally:
        # Always release after setting pin value
        led_line.release()


def test():
    seconds = 5
    times = seconds * PWM_FREQUENCY
    on_period = MAX_PERIOD
    off_period = PWM_PERIOD - on_period

    try:
        print("Lights on")
        for _ in range(times):
            on()
            sleep(on_period)
            off()
            sleep(off_period)
    finally:
        print("Lights off")
        off()

    return {"message": "Lights tested"}

def run_lights(duration, brightness):
    """
    Runs video lights using PWM over a set duration using a set brightness
    """
    
    on_period = ((MAX_PERIOD - MIN_PERIOD) * brightness / 100) + MIN_PERIOD
    off_period = PWM_PERIOD - on_period

    repeat = around(duration / PWM_PERIOD, 0)
    t1 = datetime.now()
    print(f"{t1} Video lights on")

    while repeat > 0:
        on()
        sleep(on_period)
        off()
        sleep(off_period)
        repeat -= 1

    t2 = datetime.now()
    print(f"{t2} Video lights off")

def night(scheduler: BackgroundScheduler):
    """
    Runs lights at night
    """
    
    CONFIG = configuration.get()["lights"]

    # Bound brightness to 100% and normalise to 1
    brightness = min(max(0, CONFIG["brightness"]), 100)/100

    # Get new sunset and sunrise times
    sunset, sunrise = sunset_sunrise()
    # Express start hour and minute as strings
    start_hour, start_min = sunset.strftime(time_format).split(":")

    print(f"sunset: {sunset}")
    print(f"sunrise: {sunrise}")
    temp = sunrise - sunset
    night_duration = temp.total_seconds()

    NIGHT_PERIOD = 3600 * 1/2 # Half an hour night scheduling period
    on_time = 60 # One minute on
    off_time = NIGHT_PERIOD - on_time

    def run_night():
        repeat = around(night_duration / NIGHT_PERIOD, 0)

        while repeat > 0:
            run_lights(on_time, brightness)
            sleep(off_time)
            repeat -= 1

    # NOTE: The night schedule has consists of two jobs: 
    # 1) Called "night" running the actual schedule
    # 2) Called "schedule_night" used to reschedule the night schedule every day at 12:00
    scheduler.add_job(run_night, trigger='cron', hour=start_hour, minute=start_min, id="night", replace_existing=True, max_instances=1)

def schedule(scheduler: BackgroundScheduler):
    """
    Enables schedules runtime for the lights
    """
    
    CONFIG = configuration.get()["lights"]
    
    # Bound brightness to 100% and normalise to 1
    brightness = min(max(0, CONFIG["brightness"]), 100)/100

    # Get only active periods
    light_periods = [period for period in CONFIG["periods"] if period["active"]]
    
    # Iterate over all video light periods
    for idx, light_period in enumerate(light_periods):
        start_time = light_period["start"]
        end_time = light_period["end"]
        start_hour, start_min = start_time.split(":")

        # Convert string to date time
        start = datetime.strptime(start_time, time_format)
        end = datetime.strptime(end_time, time_format)

        # Determine the duration of light period
        temp = end - start
        duration = temp.total_seconds()

        # Add job with id so it is easier to remove later
        job_id = "light" + str(idx)
        scheduler.add_job(run_lights, trigger='cron', hour=start_hour, minute=start_min, args=[duration, brightness], id=job_id, replace_existing=True, max_instances=10)
