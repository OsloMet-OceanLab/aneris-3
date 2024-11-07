"""
author: @rambech
"""

import gpiod as GPIO
from time import sleep

# Setup PWM pin
UVC_pin = 13
chip = GPIO.Chip('gpiochip4')
uvc_line = chip.get_line(UVC_pin)

def on():
    try:
        uvc_line.request(consumer="LED", type=GPIO.LINE_REQ_DIR_OUT)
        uvc_line.set_value(1)
    finally:
        uvc_line.release()

def off():
    try:
        uvc_line.request(consumer="LED", type=GPIO.LINE_REQ_DIR_OUT)
        uvc_line.set_value(0)
    finally:
        uvc_line.release()

def test():
    try:
        # print("UVC light on!")
        yield "UVC light on"
        on()
        sleep(5)
    finally:
        off()
        print("UVC light off")
