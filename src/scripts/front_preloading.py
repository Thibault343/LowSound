#**************************************************
# This script is used to pre-load the front-end of the application.
# It initializes loads the settings.
#***************************************************
import json
import flet


def load_settings():
    try:
        with open("storage\data\settings.json", "r") as f:
                settings = json.load(f)
        
        print(settings)
        return settings
    except FileNotFoundError:
        print("Settings file not found. Using default settings.")
        return {"device": "default_device"}

settings = load_settings()

def load_settings_page(dropdown):
    global settings
    dropdown.value = settings.get("device")
    """Load settings from a JSON file."""
    

def load_theme(page):
    global settings
    theme_name = settings.get("default_theme")  # Utiliser "default_theme" par défaut
    print(f"Thème load by default : {theme_name}")
    # try:
    #     with open(f"storage\data\themes\{theme_name}.json", "r") as f:
    #         default_theme = json.load(f)
    #         print(default_theme)
    # except FileNotFoundError:
    #     print("Settings file not found. Using default settings.")

