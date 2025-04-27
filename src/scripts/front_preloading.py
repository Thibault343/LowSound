#**************************************************
# This script is used to pre-load the front-end of the application.
# It initializes loads the settings.
#***************************************************
import json



def load_settings(dropdown):
    """Load settings from a JSON file."""
    try:
        with open("storage\data\settings.json", "r") as f:
            settings = json.load(f)

        dropdown.value = settings.get("device")
        return settings
    except FileNotFoundError:
        print("Settings file not found. Using default settings.")
        return {"device": "default_device"}


