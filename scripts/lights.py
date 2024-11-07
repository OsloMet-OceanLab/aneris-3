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
    string_periods = configuration.get()["lights"]["periods"]
    periods = []

    # Convert periods from string to datetime.time objects
    for string_period in string_periods:
        start = utils.string2datetime(string_period["start"])
        end = utils.string2datetime(string_period["end"])

        period = {"start": start, "end": end, "active": string_period["active"]}
        periods.append(period)
        
    while True:
        current_time = datetime.datetime.now().time()

        for period in periods:
            if (period["start"] <= current_time <= period["end"]) and period["active"]:
                on()
            else:
                off()
