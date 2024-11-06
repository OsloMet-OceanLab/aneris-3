import gpiod as GPIO
from time import sleep

# TODO: Add reset time to config
reset_time = 200


DAISY_PIN = 15
chip = GPIO.Chip('gpiochip4')
daisy_line = chip.get_line(DAISY_PIN)
daisy_line.request(consumer="LED", type=GPIO.LINE_REQ_DIR_OUT)

CAMERA_PIN = 14
chip = GPIO.Chip('gpiochip4')
camera_line = chip.get_line(CAMERA_PIN)
camera_line.request(consumer="LED", type=GPIO.LINE_REQ_DIR_OUT)


def reset_daisy():
    daisy_line.set_value(1)
    sleep(reset_time)
    daisy_line.set_value(0)


def reset_camera():
    camera_line.set_value(1)
    sleep(reset_time)
    camera_line.set_value(0)
