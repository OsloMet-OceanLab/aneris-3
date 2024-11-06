import json


def get():
    return {"message": "I got got!"}


def set(param):
    with open("configuration/config.json", "r") as file:
        config = json.load(file)

    print(f"param: {param}")

    if config["test_param"] == param:
        return {"message": "Same value, no need to update"}

    config["test_param"] = param

    with open("configuration/config.json", "w") as file:
        json.dump(config, file, indent=4)

    # Acknowledge that parameter has been set
    if config["test_param"] == param:
        return {"message": "Test param set!"}
    else:
        return {"message": "Test param not updated"}
