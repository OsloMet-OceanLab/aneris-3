from flask import Flask, render_template, request, jsonify
# from scripts import read_pressure, control_lights
from scripts import configuration  # , relay
from tests import tests

app = Flask(__name__)


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


@app.route("/set_camera_relay", methods=["POST"])
def set_camera_relay():
    """
    Toggle camera relay
    """

    # camera_relay_state = request.json.get("camera_relay_state")
    # print(f"camera_relay_state: {camera_relay_state}")
    # verify_camera_state = relay.toggle_camera(camera_relay_state)
    # return jsonify(verify_camera_state=verify_camera_state)


@app.route("/set_daisy_relay", methods=["POST"])
def set_daisy_relay():
    """
    Toggle daisy relay
    """

    # daisy_relay_state = request.json.get("daisy_relay_state")
    # print(f"camera_daisy_state: {daisy_relay_state}")
    # verify_daisy_state = relay.toggle_camera(daisy_relay_state)
    # return jsonify(verify_camera_state=verify_daisy_state)


@app.route("/get_temp", methods=["GET"])
def get_temp():
    """
    Get temperature outside enclosure
    """

    # temperature = sensors.read_temperature()
    temperature = 1
    return jsonify(temperature=temperature)


@app.route("/get_pres", methods=["GET"])
def get_pres():
    """
    Get pressure outside enclosure
    """

    # pressure = sensors.read_pressure()
    pressure = 2
    print(pressure)
    return jsonify(pressure=pressure)


if __name__ == "__main__":
    app.run(debug=True)
