# TODO: Add control lights config in file

"""
author: @rambech
"""

import gpiod as GPIO
from time import sleep
from lib import utils
import datetime
from scripts import configuration

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
        led_line.request(consumer="LED", type=GPIO.LINE_REQ_DIR_OUT)
        brightness = configuration.get()["lights"]["brightness"]
        on_period = ((MAX_PERIOD - MIN_PERIOD) * brightness / 100) + MIN_PERIOD
        off_period = PWM_PERIOD - on_period

        led_line.set_value(1)
        sleep(on_period)
        led_line.set_value(0)
        sleep(off_period)
    except OSError:
        print("Not able to access GPIO")
        pass
    finally:
        # Only try to turn off again if led_line is registered
        try:
            led_line.set_value(0)
        except:
            pass

        led_line.release()


def off():
    try:
        led_line.request(consumer="LED", type=GPIO.LINE_REQ_DIR_OUT)
        led_line.set_value(0)
    except OSError:
        print("Not able to access GPIO")
        pass
    finally:
        # Only try to turn off again if led_line is registered
        try:
            led_line.set_value(0)
        except:
            pass

        led_line.release()



def test():
    seconds = 5
    times = seconds * PWM_FREQUENCY

    try:
        print("Lights on")
        for _ in range(times):
            on()
    finally:
        print("Lights off")
        off()

    return {"message": "Lights tested"}


def scheduled():
    """
    Enables schedules runtime for the lights
    """
    
    CONFIG = configuration.get()["lights"]

    periods = CONFIG["periods"]

    scheduler = BackgroundScheduler()
    scheduler.configure(timezone=utc)
    
    for period in periods:
        start_time = period["start"]
        start_hour, start_min = start_time.split(":")

        end_time = period["end"]
        end_hour, end_min = start_time.split(":")

        scheduler.add_job(on, trigger='cron', hour=start_hour, minute=start_min)
        scheduler.add_job(off, trigger="cron", hour=end_hour, minute=end_min)

    scheduler.start()
