from flask import Flask, render_template, request, jsonify
from scripts import lights, uvc, configuration, relay # sensors
from pytz import timezone, utc
from apscheduler.schedulers.background import BackgroundScheduler

cet = timezone("CET")
scheduler = BackgroundScheduler()
scheduler.configure(timezone=cet)

app = Flask(__name__)

def schedule():
    if scheduler.running:
        scheduler.remove_all_jobs()
    else:
        scheduler.start()

    lights.schedule(scheduler)
    uvc.schedule(scheduler)

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/get_config', methods=['GET'])
def get_config():
    """
    Get UVC and lights configuration
    """

    config = configuration.get()
    print(config)
    return jsonify(config=config)


@app.route("/set_config", methods=["POST"])
def set_config():
    """
    Set UVC and lights configuration
    """

    new_config = request.json.get("newConfig")
    print(f"new config: {new_config}")
    ack = configuration.set(new_config)
    return jsonify(ack=ack)


@app.route("/restart_schedule", methods=["POST"])
def restart_schedule():
    """
    Restart video lights after a new configuration has been set
    """

    print("Restart schedule")
    schedule()
    res = {"message": "Shedule restarted"}

    return jsonify(res=res)


@app.route("/test_light", methods=["POST"])
def test_light():
    """
    Test video lights
    """

    ack =  lights.test()

    return jsonify(ack)


@app.route("/test_UVC", methods=["POST"])
def test_UVC():
    """
    Test UVC anti-biofouling light
    """

    ack = uvc.test()

    return ack


@app.route("/reboot_camera", methods=["POST"])
def reboot_camera():
    """
    Reboot camera
    """

    print("Reboot camera")
    verify_camera_reboot = relay.reboot_camera()
    return jsonify(verify_camera_reboot=verify_camera_reboot)


@app.route("/reboot_daisy", methods=["POST"])
def reboot_daisy():
    """
    Reboot daisy
    """

    print("Reboot daisy chain")
    verify_daisy_reboot = relay.reboot_daisy()
    return jsonify(verify_daisy_reboot=verify_daisy_reboot)


@app.route("/set_camera_relay", methods=["POST"])
def set_camera_relay():
    """
    Toggle camera relay
    """

    camera_relay_state = request.json.get("cameraRelayState")
    print(f"Camera relay: {camera_relay_state}")
    verify_camera_state = relay.toggle_camera(camera_relay_state)
    return jsonify(verify_camera_state=verify_camera_state)


@app.route("/set_daisy_relay", methods=["POST"])
def set_daisy_relay():
    """
    Toggle daisy relay
    """

    daisy_relay_state = request.json.get("daisyRelayState")
    print(f"Daisy relay: {daisy_relay_state}")
    verify_daisy_state = relay.toggle_daisy(daisy_relay_state)
    return jsonify(verify_daisy_state=verify_daisy_state)


@app.route("/get_temp", methods=["GET"])
def get_temp():
    """
    Get temperature outside enclosure
    """

    # temperature = sensors.read_temperature
    # return jsonify(temperature)

    raise NotImplementedError


@app.route("/get_pres", methods=["GET"])
def get_pres():
    """
    Get pressure outside enclosure
    """

    # pressure = sensors.read_pressure()
    # return jsonify(pressure=pressure)

    raise NotImplementedError


if __name__ == "__main__":
    app.run(debug=True)
