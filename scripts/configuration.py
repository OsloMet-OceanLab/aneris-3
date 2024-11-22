import json


def get():
    # Send current config
    with open("configuration/config.json", "r") as file:
        config = json.load(file)

    if config is not None:
        return config
    else:
        print("No valid configuration found")
        return None


def set(new_config):
    # TODO: Implement check for valid option
    if type(new_config) is not dict:
        return f"Was not able to update config, datatype was {type(new_config).__name__}"

    # Save config
    try:
        with open("configuration/config.json", "w") as file:
            json.dump(new_config, file, indent=4)

        return "Config updated"
    except Exception as e:
        return f"Was not able to update config, error {e}"
