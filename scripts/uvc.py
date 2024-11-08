"""
author: @rambech
"""

import gpiod as GPIO
from time import sleep
from scripts import configuration
from apscheduler.schedulers.background import BackgroundScheduler


# Setup GPIO pin
UVC_pin = 25
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


def scheduled():
    """
    Enables schedules runtime for the lights
    """
    
    CONFIG = configuration.get()["uvc"]
    
    start_time = CONFIG["time"]
    start_hour, start_min = start_time.split(":")
    duration = CONFIG["duration"]
    duty_cycle = CONFIG["duty_cycle"]
    period = CONFIG["period"]

    def run_uvc():
        on_time = period * duty_cycle
        off_time = period - on_time
        repeat = duration / period

        while repeat > 0:
            on()
            sleep(on_time)
            off()
            sleep(off_time)
            repeat -= 1

    scheduler = BackgroundScheduler()
    scheduler.configure(timezone=utc)
    scheduler.add_job(run_uvc, trigger='cron', hour=start_hour, minute=start_min)

    scheduler.start()
