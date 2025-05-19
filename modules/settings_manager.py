import json
# ------------------------------------------------
# Function: save_settings
# Arguments:
#   - dropdown_device (str): The selected audio output device.
#   - dropdown_theme (str): The selected default theme.
# Description:
#   Loads existing settings from 'settings.json',
#   updates the audio device and theme if needed,
#   then saves the new values back to the file.
# ------------------------------------------------
def save_settings(dropdown_device, dropdown_theme):
    with open('data/settings.json', 'r+') as f:
        settings = json.load(f)
        if settings['device'] != dropdown_device:
            settings['device'] = dropdown_device
        if settings['default_theme'] != dropdown_theme:
            settings['default_theme'] = dropdown_theme
            
        f.seek(0)
        json.dump(settings, f, indent=4)
        f.truncate()
