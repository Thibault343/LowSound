import json

def save_settings(dropdown_device, dropdown_theme):
    with open('data/settings.json', 'r+') as f:
        settings = json.load(f)
        if settings['device'] != dropdown_device.value:
            settings['device'] = dropdown_device.value
        if settings['default_theme'] != dropdown_theme.value:
            settings['default_theme'] = dropdown_theme.value
        f.seek(0)
        json.dump(settings, f, indent=4)
        f.truncate()
