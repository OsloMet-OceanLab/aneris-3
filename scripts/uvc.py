# TODO: Add uvc config file

"""
author: @rambech
"""

import gpiod as GPIO
from time import sleep

# Setup PWM pin
UVC_pin = 13
chip = GPIO.Chip('gpiochip4')
uvc_line = chip.get_line(UVC_pin)
uvc_line.request(consumer="LED", type=GPIO.LINE_REQ_DIR_OUT)

PWM_frequency = 100          # Hertz
PWM_period = 1/PWM_frequency  # Seconds
brightness = 50              # Percent
max_period = 1900 * 1e-6     # 1900 microseconds
min_period = 1100 * 1e-6     # 1100 microseconds
on_period = ((max_period - min_period) * brightness / 100) + min_period
off_period = PWM_period - on_period

# Display period information
print(f"PWM_period: {PWM_period * 1e6}")
print(f"on_period: {on_period * 1e6}")
print(f"off_period: {off_period * 1e6}")

try:
    if (on_period > 0):
        print("Lights on")
    else:
        print("Lights off")

    while True:
        uvc_line.set_value(1)
        sleep(on_period)
        uvc_line.set_value(0)
        sleep(off_period)
finally:
    print("Lumen script terminated")
    uvc_line.release()
