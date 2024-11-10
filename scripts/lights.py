"""
author: @rambech
"""

import gpiod as GPIO
from time import sleep
from numpy import around
from datetime import datetime
from scripts import configuration
from apscheduler.schedulers.background import BackgroundScheduler

# Setup PWM pin
PWM_pin = 12
chip = GPIO.Chip('gpiochip4')
led_line = chip.get_line(PWM_pin)

PWM_FREQUENCY = 100          # Hertz
PWM_PERIOD = 1/PWM_FREQUENCY  # Seconds
# brightness = 50              # Percent
MAX_PERIOD = 1900 * 1e-6     # 1900 microseconds
MIN_PERIOD = 1100 * 1e-6     # 1100 microseconds


def on():
    try:
        print("Lights on")
        led_line.request(consumer="LED", type=GPIO.LINE_REQ_DIR_OUT)
        led_line.set_value(1)
    finally:
        led_line.release()


def off():
    try:
        print("Lights off")
        led_line.request(consumer="LED", type=GPIO.LINE_REQ_DIR_OUT)
        led_line.set_value(0)
    finally:
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


def schedule(scheduler: BackgroundScheduler):
    """
    Enables schedules runtime for the lights
    """
    
    CONFIG = configuration.get()["lights"]

    time_format = "%H:%M"
    # brightness = min(max(0, CONFIG["brightness"]), 100)/100
    # Get only active periods
    light_periods = [period for period in CONFIG["periods"] if period["active"]]
    # on_period = ((MAX_PERIOD - MIN_PERIOD) * brightness / 100) + MIN_PERIOD
    # off_period = PWM_PERIOD - on_period

    # print(f"on_time: {on_period}")
    # print(f"off_time: {off_period}")

    def run_lights(duration):
        # repeat = around(duration / PWM_PERIOD, 0)
        # print(f"repeat: {repeat}")
        on_period = duration

        on()
        sleep(on_period)
        off()
        # while repeat > 0:
        #     on()
        #     sleep(on_period)
        #     off()
        #     sleep(off_period)
        #     repeat -= 1
    
    for light_period in light_periods:
        start_time = light_period["start"]
        end_time = light_period["end"]
        start_hour, start_min = start_time.split(":")

        start = datetime.strptime(start_time, time_format)
        end = datetime.strptime(end_time, time_format)
        temp = end - start
        duration = temp.total_seconds()
        print(f"duration: {duration}")

        scheduler.add_job(run_lights, trigger='cron', hour=start_hour, minute=start_min, args=[duration])
