import gpiod as GPIO
from time import sleep
from scripts import configuration


DAISY_PIN = 15
chip = GPIO.Chip('gpiochip4')
daisy_line = chip.get_line(DAISY_PIN)

CAMERA_PIN = 14
chip = GPIO.Chip('gpiochip4')
camera_line = chip.get_line(CAMERA_PIN)

def daisy_on():
    # Daisy is connected to normally closed
    try:
        daisy_line.request(consumer="LED", type=GPIO.LINE_REQ_DIR_OUT)
        daisy_line.set_value(0)
    finally:
        daisy_line.release()


def camera_on():
    # Camera is also connected to normally closed
    try:
        camera_line.request(consumer="LED", type=GPIO.LINE_REQ_DIR_OUT)
        camera_line.set_value(0)
    finally:
        camera_line.release()


def daisy_off():
    try:
        daisy_line.request(consumer="LED", type=GPIO.LINE_REQ_DIR_OUT)
        daisy_line.set_value(1)
    finally:
        daisy_line.release()


def camera_off():
    try:
        camera_line.request(consumer="LED", type=GPIO.LINE_REQ_DIR_OUT)
        camera_line.set_value(1)
    finally:
        camera_line.release()


def reboot_daisy():
    try: 
        reset_time = configuration.get()["reset_time"]
    except:
        reset_time = 10
        
    daisy_off()
    sleep(reset_time)
    daisy_on()


def reboot_camera():
    try: 
        reset_time = configuration.get()["reset_time"]
    except:
        reset_time = 10

    camera_off()
    sleep(reset_time)
    camera_on()
    

def toggle_camera():
    CONFIG = configuration.get()
    on = CONFIG["relay"]["camera"]

    if not on:
        camera_off()
        return False
    else:
        camera_on()
        return True

def toggle_daisy():
    CONFIG = configuration.get()
    on = CONFIG["relay"]["daisy"]

    if not on:
        daisy_off()
        return False
    else:
        daisy_on()
        return True