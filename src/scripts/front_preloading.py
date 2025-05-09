#**************************************************
# This script is used to pre-load the front-end of the application.
# It initializes loads the settings.
#***************************************************
import json
import flet
import os


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

def load_settings_page(dropdown_device, dropdown_default_theme):
    global settings
    dropdown_device.value = settings.get("device")
    dropdown_default_theme.value = settings.get("default_theme")
    """Load settings from a JSON file."""
    

def get_theme_colors(theme):
    global settings
    if theme == None:
        theme_name = settings.get("default_theme")  # Utiliser "default_theme" par défaut
    else: 
        theme_name = theme.value
    try:
        with open(f"storage/data/themes/{theme_name}.json", "r") as f:
            default_theme = json.load(f)
            return default_theme
    except FileNotFoundError:
        print("Settings file not found. Using default settings.")

# load the theme list for the dropdown
def get_theme_list():
    theme_list = []
    theme_dir = "storage/data/themes"
    try:
        for file_name in os.listdir(theme_dir):
            if file_name.endswith(".json"):
                theme_list.append(file_name[:-5])  # Remove the ".json" extension
        return theme_list
    except FileNotFoundError:
        print(f"Directory {theme_dir} not found.")
        return []
