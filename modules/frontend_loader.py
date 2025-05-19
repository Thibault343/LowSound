#**************************************************
# This script is used to pre-load the front-end of the application.
# It initializes loads the settings.
#***************************************************
import json
import flet as ft
import os

# ------------------------------------------------
# Function: load_settings
# Arguments: None
# Description:
#   Loads the application settings from the "data/settings.json" file.
#   If the file is not found, returns default settings.
# Returns:
#   A dictionary with settings such as audio device and theme preferences.
# ------------------------------------------------
def load_settings():
    try:
        with open("data/settings.json", "r") as f:
                settings = json.load(f)
        
        return settings
    except FileNotFoundError:
        print("Settings file not found. Using default settings.")
        return {"device": "default_device"}

settings = load_settings()

# ------------------------------------------------
# Function: load_settings_page
# Arguments:
#   - dropdown_device: The dropdown component for selecting the audio device.
#   - dropdown_default_theme: The dropdown component for selecting the theme.
# Description:
#   Loads the saved settings into the UI elements by updating their selected values.
#   Uses the global `settings` dictionary to populate each dropdown.
# ------------------------------------------------
def load_settings_page(dropdown_device, dropdown_default_theme):
    global settings
    dropdown_device.value = settings.get("device")
    dropdown_default_theme.value = settings.get("default_theme")
    
# ------------------------------------------------
# Function: get_theme_colors
# Arguments:
#   - theme (str or None): Name of the theme to load. If None, falls back to the default theme from settings.
# Description:
#   Loads the color configuration of the specified theme from a JSON file in the `data/themes/` directory.
#   If the theme file is not found, prints an error message and returns None.
# Returns:
#   - dict: A dictionary containing the theme colors if loaded successfully.
#   - None: If the theme file is not found.
# ------------------------------------------------
def get_theme_colors(theme):
    global settings
    if theme == None:
        theme_name = settings.get("default_theme")  # Utiliser "default_theme" par défaut
    else: 
        theme_name = theme
    try:
        with open(f"data/themes/{theme_name}.json", "r") as f:
            default_theme = json.load(f)
            return default_theme
    except FileNotFoundError:
        print("Settings file not found. Using default settings.")

# ------------------------------------------------
# Function: get_theme_list
# Description:
#   Scans the 'data/themes' directory and returns a list of all available theme names.
#   Each theme corresponds to a JSON file in that directory.
# Returns:
#   - list[str]: A list of theme names (without the .json extension).
#   - []: If the directory does not exist or an error occurs.
# ------------------------------------------------
def get_theme_list():
    theme_list = []
    theme_dir = "data/themes"
    try:
        for file_name in os.listdir(theme_dir):
            if file_name.endswith(".json"):
                theme_list.append(file_name[:-5])  # Remove the ".json" extension
        return theme_list
    except FileNotFoundError:
        print(f"Directory {theme_dir} not found.")
        return []
    
