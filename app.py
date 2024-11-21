from flask import Flask, render_template, request, jsonify
from scripts import lights, uvc, configuration, relay # sensors
from lib import utils
from pytz import timezone
from apscheduler.schedulers.background import BackgroundScheduler

cet = timezone("CET")
scheduler = BackgroundScheduler()
scheduler.configure(timezone=cet)
scheduler.start()

app = Flask(__name__)


def schedule():
    """
    Sets schedules from video lights and UVC timetables
    """

    for job in scheduler.get_jobs():
        # Only remove jobs related to the UI time table
        if job.id[:3] == "uvc" or job.id[:3] == "lig":
            scheduler.remove_job(job.id)
            
    # Schedule lights
    lights.schedule(scheduler)
    uvc.schedule(scheduler)

    # Display active jobs in terminal
    print(f"Current background processes:")
    utils.print_jobs(scheduler)


def schedule_night():
    # Update scheduler once a day in order to keep sunrise and sunset up to date
    # Triggers mid-day in order to avoid conflicts with lights at night
    scheduler.add_job(schedule_night, trigger='cron', hour=12, minute=0, id="schedule_night", replace_existing=True)
    lights.night(scheduler)

    print(f"Current background processes:")
    utils.print_jobs(scheduler)


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
    res = {"message": "Schedule restarted"}

    return jsonify(res=res)

@app.route("/set_night_schedule", methods=["POST"])
def toggle_night_schedule():
    """
    Toggles the video lights at night
    """

    print("Toggle night video light schedule")

    # Get state from UI
    night_schedule_state = request.json.get("nightScheduleState")

    # Update configuration with night schedule state
    CONFIG = configuration.get()
    CONFIG["lights"]["night"] = night_schedule_state
    configuration.set(CONFIG)

    night_schedule_feedback = CONFIG["lights"]["night"]

    if night_schedule_state:
        # Schedule night light if commanded True from UI
        schedule_night()
    elif scheduler.running:
        print("Scheduler running")
        # Check if night light is running when commanded False from UI
        scheduler.remove_job(job_id="night")
        scheduler.remove_job(job_id="schedule_night")

    return jsonify(night_schedule_feedback=night_schedule_feedback)

    

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

    print("Toggle camera relay")

    # Get state from UI
    camera_relay_state = request.json.get("cameraRelayState")
    
    # Update configuration with night schedule state
    CONFIG = configuration.get()
    CONFIG["relay"]["camera"] = camera_relay_state
    configuration.set(CONFIG)

    camera_state_feedback = relay.toggle_camera()
    return jsonify(camera_state_feedback=camera_state_feedback)


@app.route("/set_daisy_relay", methods=["POST"])
def set_daisy_relay():
    """
    Toggle daisy relay
    """

    print("Toggle daisy relay")

    # Get state from UI
    daisy_relay_state = request.json.get("daisyRelayState")
    
    # Update configuration with night schedule state
    CONFIG = configuration.get()
    CONFIG["relay"]["daisy"] = daisy_relay_state
    configuration.set(CONFIG)

    daisy_state_feedback = relay.toggle_daisy()
    return jsonify(daisy_state_feedback=daisy_state_feedback)


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
