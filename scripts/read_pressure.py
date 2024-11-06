import kellerLD
import time

bar100_sensor = kellerLD.KellerLD()

try:
    bar100_sensor.init()
    time.sleep(0.008)  # Need additional pause
    print("100 bar pressure sensor initialized")
except OSError:
    use_bar100_sensor = False
    print("100 bar pressure sensor could not be initialized")

if not use_bar100_sensor:
    print("No blue robotics pressure sensors connected")
    exit(1)


def read_temperature():
    try:
        if use_bar100_sensor:
            bar100_sensor.read()
            return {"message": bar100_sensor.temperature()}

    except Exception as e:
        print(e)
        print("Sensor read failed!")
        exit(1)


def read_pressure():
    try:
        if use_bar100_sensor:
            bar100_sensor.read()
            return {"message": bar100_sensor.pressure()}

    except Exception as e:
        print(e)
        print("Sensor read failed!")
        exit(1)
