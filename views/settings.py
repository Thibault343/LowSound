import flet as ft
from modules import frontend_loader


# ------------------------------------------------
# Function: build
# Arguments:
#   - container: The UI container where the settings controls will be displayed.
#   - devices (list): List of available audio devices (strings) for the dropdown.
#   - themes (list): List of available themes (strings) for the dropdown.
#   - on_save (function): Callback function to call when the "Save" button is clicked,
#                        receives selected device and theme as arguments.
# Description:
#   Builds the settings UI inside the provided container:
#   - Loads current settings from frontend_loader.
#   - Creates dropdown menus for selecting audio device and theme, preselected with saved values.
#   - Adds a Save button which triggers the on_save callback with the selected options.
# ------------------------------------------------
def build(container, devices, themes, on_save):

    settings = frontend_loader.load_settings()
    dropdown_device = ft.Dropdown(options=[ft.dropdown.Option(d) for d in devices], value=settings['device'])
    dropdown_theme = ft.Dropdown(options=[ft.dropdown.Option(t) for t in themes], value=settings['default_theme'])

    container.controls.clear()
    container.controls.extend([
        ft.Text("Settings", size=24, weight=ft.FontWeight.BOLD),
        ft.Text("Audio device:"),
        dropdown_device,
        ft.Text("Theme:"),
        dropdown_theme,
        ft.ElevatedButton(text="Save", on_click=lambda _: on_save(dropdown_device.value, dropdown_theme.value))
    ])
    print("Loading page : Settings ")
