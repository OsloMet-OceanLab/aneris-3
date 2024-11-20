function getConfig() {
    fetch('/get_config')
        .then(response => response.json())
        .then(data => {
            // Load lights configuration
            const periods = data.config["lights"]["periods"];
            periods.forEach(period => {
                addTimePeriod(startTime = period["start"], endTime = period["end"], active = period["active"])
            });
            document.getElementById("reset_time").value = data.config["reset_time"];
            document.getElementById("toggle_camera").checked = data.config["relay"]["camera"];
            document.getElementById("toggle_daisy").checked = data.config["relay"]["daisy"];
            document.getElementById("light_brightness").value = data.config["lights"]["brightness"];
            document.getElementById("toggle_night_schedule").checked = data.config["lights"]["night"];

            // Load UVC configuration
            const uvcPeriods = data.config["uvc"]["periods"];
            uvcPeriods.forEach(period => {
                addUVCTimePeriod(startTime = period["start"], endTime = period["end"], active = period["active"])
            });
            document.getElementById('duty_cycle').value = data.config["uvc"]["duty_cycle"];
        })
        .catch(error => console.error("Error loading data", error));
}

function setConfig() {
    // Make list of dicts with light time periods
    const periods = [];
    const periodDivs = document.querySelectorAll('.time-period');

    periodDivs.forEach(div => {
        const startTime = div.querySelector('.start-time').value;
        const endTime = div.querySelector('.end-time').value;
        const active = div.dataset.active === "true";

        if (startTime && endTime) {  // Only add if both times are set
            periods.push({ start: startTime, end: endTime, active: active });
        }
    });

    // Make list of dicts with UVC time periods
    const uvcPeriods = [];
    const uvcPeriodDivs = document.querySelectorAll('.uvc-time-period');

    uvcPeriodDivs.forEach(div => {
        const uvcStartTime = div.querySelector('.uvc-start-time').value;
        const uvcEndTime = div.querySelector('.uvc-end-time').value;
        const uvcActive = div.dataset.active === "true";

        if (uvcStartTime && uvcEndTime) {  // Only add if both times are set
            uvcPeriods.push({ start: uvcStartTime, end: uvcEndTime, active: uvcActive });
        }
    });

    // Build new configuration
    const newConfig = {
        reset_time: parseFloat(document.getElementById("reset_time").value, 10),
        relay: {
            camera: document.getElementById("toggle_camera").checked,
            daisy: document.getElementById("toggle_daisy").checked
        },
        lights: {
            periods: periods,
            brightness: parseInt(document.getElementById("light_brightness").value, 10),
            night: document.getElementById("toggle_night_schedule").checked,
        },
        uvc: {
            periods: uvcPeriods,
            duty_cycle: parseInt(document.getElementById("duty_cycle").value, 10),
        }
    }

    // Send new configuration
    fetch('/set_config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ newConfig })

    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('ack').innerText = data.ack;
            // Restart video lights and uvc after setting configuration
            restart_schedule();
        })
}

function restart_schedule() {
    // Restart video lights and UVC
    fetch('/restart_schedule', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('res').innerText = data.res.message;
        });
}

function addTimePeriod(startTime = null, endTime = null, active = true) {
    // Create a new div to hold the start and end time inputs
    const container = document.getElementById('timePeriodsContainer');
    const periodDiv = document.createElement('div');
    periodDiv.dataset.active = active; // Initalise active
    periodDiv.classList.add('time-period');

    // Create start time input
    const startTimeInput = document.createElement('input');
    startTimeInput.type = 'time';
    startTimeInput.classList.add('start-time');
    startTimeInput.value = startTime ? startTime : "";
    startTimeInput.placeholder = "Start Time"

    // Create end time input
    const endTimeInput = document.createElement('input');
    endTimeInput.type = 'time';
    endTimeInput.classList.add('end-time');
    endTimeInput.value = endTime ? endTime : "";
    endTimeInput.placeholder = 'End Time';

    // Activate/Deactivate button
    const toggleButton = document.createElement('button');
    toggleButton.innerText = active ? 'Deactivate' : 'Activate';
    toggleButton.onclick = function () {
        const isActive = periodDiv.dataset.active === "true";
        periodDiv.dataset.active = isActive ? "false" : "true";
        toggleButton.innerText = isActive ? 'Activate' : 'Deactivate';
        periodDiv.classList.toggle('active', !isActive);
        setConfig();
    };

    // Create remove button
    const removeButton = document.createElement('button');
    removeButton.innerText = 'Remove';
    removeButton.onclick = function () {
        container.removeChild(periodDiv);
    };

    // Append inputs and button to the period div
    periodDiv.appendChild(startTimeInput);
    periodDiv.appendChild(endTimeInput);
    periodDiv.appendChild(toggleButton);
    periodDiv.appendChild(removeButton);

    // Append the period div to the main container
    container.appendChild(periodDiv);
}

function addUVCTimePeriod(startTime = null, endTime = null, dutyCycle = null, active = true) {
    // Create a new div to hold the start and end time inputs
    const container = document.getElementById('uvcTimePeriodsContainer');
    const periodDiv = document.createElement('div');
    periodDiv.dataset.active = active; // Initalise active
    periodDiv.classList.add('uvc-time-period');

    // Create start time input
    const startTimeInput = document.createElement('input');
    startTimeInput.type = 'time';
    startTimeInput.classList.add('uvc-start-time');
    startTimeInput.value = startTime ? startTime : "";
    startTimeInput.placeholder = "Start Time"

    // Create end time input
    const endTimeInput = document.createElement('input');
    endTimeInput.type = 'time';
    endTimeInput.classList.add('uvc-end-time');
    endTimeInput.value = endTime ? endTime : "";
    endTimeInput.placeholder = 'End Time';

    // Activate/Deactivate button
    const toggleButton = document.createElement('button');
    toggleButton.innerText = active ? 'Deactivate' : 'Activate';
    toggleButton.onclick = function () {
        const isActive = periodDiv.dataset.active === "true";
        periodDiv.dataset.active = isActive ? "false" : "true";
        toggleButton.innerText = isActive ? 'Activate' : 'Deactivate';
        periodDiv.classList.toggle('active', !isActive);
        setConfig();
    };

    // Create remove button
    const removeButton = document.createElement('button');
    removeButton.innerText = 'Remove';
    removeButton.onclick = function () {
        container.removeChild(periodDiv);
    };

    // Append inputs and button to the period div
    periodDiv.appendChild(startTimeInput);
    periodDiv.appendChild(endTimeInput);
    periodDiv.appendChild(toggleButton);
    periodDiv.appendChild(removeButton);

    // Append the period div to the main container
    container.appendChild(periodDiv);

    // // Set the active class if the period is active
    // if (active) {
    //     periodDiv.classList.add('active');
    // }
}

function getTempAndPres() {
    fetch('/get_temp', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            document.getElementById('temperature').innerText = data.temperature;
        });

    fetch('/get_pres', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            document.getElementById('pressure').innerText = data.pressure;
        });
}

function rebootCamera() {
    fetch('/reboot_camera', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('verify_camera_reboot').innerText = data.verify_camera_reboot;
        });
}

function rebootDaisy() {
    fetch('/reboot_daisy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('verify_daisy_reboot').innerText = data.verify_daisy_reboot;
        });
}

function setCameraRelay(state) {
    fetch('/set_camera_relay', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cameraRelayState: state })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('toggle_camera').innerText = data.camera_state_feedback;
        });
}

function setDaisyRelay(state) {
    fetch('/set_daisy_relay', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ daisyRelayState: state })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('toggle_daisy').innerText = data.daisy_state_feedback;
        });
}

function setNightScheduleState(state) {
    // Toggle night schedule for video lights
    fetch("/set_night_schedule", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nightScheduleState: state })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("toggle_night_schedule").value = data.night_schedule_feedback
        })
}

function testLight() {
    fetch('/test_light', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').innerText = data.result.message;
        });
}

function testUVC() {
    const test_param = confirm("WARNING, HARMFUL UVC LIGHT! Are you sure if you want to trigger UVC light for 5 seconds?");
    fetch('/test_UVC', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ test_param: test_param })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').innerText = data.result.message;
        });
}

// Event lisners
// Load config when config gets loaded
window.onload = getConfig;
document.getElementById('toggle_camera').addEventListener('change', function () {
    const isChecked = this.checked;
    setCameraRelay(isChecked); // Call the function with the current state
});
document.getElementById('toggle_daisy').addEventListener('change', function () {
    const isChecked = this.checked;
    setDaisyRelay(isChecked); // Call the function with the current state
});
document.getElementById('toggle_night_schedule').addEventListener('change', function () {
    const isChecked = this.checked;
    setNightScheduleState(isChecked); // Call the function with the current state
});