from flask import Flask, render_template, request, jsonify
# from scripts import read_pressure, control_lights
from scripts import configuration
from tests import tests

# TODO: Implement list of times

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/get_config', methods=['GET'])
def get_config():
    config = configuration.get()
    print(config)
    return jsonify(config=config)


@app.route("/set_config", methods=["POST"])
def set_config():
    new_config = request.json.get("newConfig")
    print(f"new config: {new_config}")
    ack = configuration.set(new_config)
    return jsonify(ack=ack)


@app.route("/get_temp", methods=["GET"])
def get_temp():
    # temperature = read_pressure.read_temperature()
    temperature = 1
    return jsonify(temperature=temperature)


@app.route("/get_pres", methods=["GET"])
def get_pres():
    # pressure = read_pressure.read_pressure()
    pressure = 2
    print(pressure)
    return jsonify(pressure=pressure)


if __name__ == "__main__":
    app.run(debug=True)
