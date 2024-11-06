# TODO: Add control lights config in file

"""
author: @rambech
"""

import gpiod as GPIO
from time import sleep
from scripts import configuration

# Setup PWM pin
PWM_pin = 18
chip = GPIO.Chip('gpiochip4')
led_line = chip.get_line(PWM_pin)
led_line.request(consumer="LED", type=GPIO.LINE_REQ_DIR_OUT)

PWM_FREQUENCY = 100          # Hertz
PWM_PERIOD = 1/PWM_FREQUENCY  # Seconds
# brightness = 50              # Percent
MAX_PERIOD = 1900 * 1e-6     # 1900 microseconds
MIN_PERIOD = 1100 * 1e-6     # 1100 microseconds


def on():
    brightness = configuration.get()["lights"]["brightness"]
    on_period = ((MAX_PERIOD - MIN_PERIOD) * brightness / 100) + MIN_PERIOD
    off_period = PWM_PERIOD - on_period

    led_line.set_value(1)
    sleep(on_period)
    led_line.set_value(0)
    sleep(off_period)


def off():
    led_line.set_value(0)
    led_line.release()


def test():
    seconds = 5

    try:
        print("Lights on")
        for _ in range(seconds):
            on()
    finally:
        print("Lights off")
        off()


def scheduled():
    while True:
        if True:
            on()
        else:
            off()
