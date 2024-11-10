"""
author: @rambech
"""

import gpiod as GPIO
from time import sleep
from numpy import around
from datetime import datetime
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


def schedule(scheduler: BackgroundScheduler):
    """
    Enables schedules runtime for the lights
    """
    
    CONFIG = configuration.get()["uvc"]
    
    time_format = "%H:%M"
    # Bound duty cycle to [0, 100] and normalise to 1
    duty_cycle = min(max(0, CONFIG["duty_cycle"]), 100)/100
    uvc_periods = [period for period in CONFIG["periods"] if period["active"]]
    period = 60
    on_time = duty_cycle * 2.5
    off_time = period - on_time

    # print(f"on_time: {on_time}")
    # print(f"off_time: {off_time}")

    def run_uvc(duration):
        repeat = around(duration / period, 0)
        t1 = datetime.now()
        print(f"{t1} UVC on")

        while repeat > 0:
            on()
            sleep(on_time)
            off()
            sleep(off_time)
            repeat -= 1

        t2 = datetime.now()
        print(f"{t2} UVC off")

    for uvc_period in uvc_periods:
        start_time = uvc_period["start"]
        end_time = uvc_period["end"]
        start_hour, start_min = start_time.split(":")

        start = datetime.strptime(start_time, time_format)
        end = datetime.strptime(end_time, time_format)
        temp = end - start
        duration = temp.total_seconds()
        # print(f"duration: {duration}")

        # scheduler.add_job(run_uvc(duration), trigger='cron', hour=start_hour, minute=start_min)
        scheduler.add_job(run_uvc, trigger='cron', hour=start_hour, minute=start_min, args=[duration])
