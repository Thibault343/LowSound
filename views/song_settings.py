import flet as ft
from modules import sound_manager

#------------------------------------------------
#   **     keybind input management     **
# - Autodetect and select mode when a user can select a keybind
# - limit the keybind possiblity
#------------------------------------------------


keybind_active = False

keybind_input = ft.TextField(
    label="Keybind",
    read_only=True,
    on_focus=lambda e: activate_keybind(True),
    on_blur=lambda e: activate_keybind(False),

)
# ------------------------------------------------
# Function: activate_keybind
# Arguments:
#   - state (bool): If True, enables key input mode for setting a keybind.
# Description:
#   Toggles keybind input mode by updating the input field accordingly.
#   When active, prompts the user to press a key.
# ------------------------------------------------
def activate_keybind(state: bool):
    global keybind_active
    keybind_active = state
    if state:
        keybind_input.value = "Press a key..."
    else:
        if keybind_input.value == "Press a key...":
            keybind_input.value = ""
    keybind_input.update()

# ------------------------------------------------
# Function: on_key_press
# Arguments:
#   - e (ft.KeyboardEvent): The keyboard event triggered by a key press.
# Description:
#   If keybind input mode is active, constructs and displays the key combination
#   (e.g., Ctrl + Shift + A) based on the pressed keys.
# ------------------------------------------------
INVALID_KEYS = ["Escape", "Tab", "Enter", "CapsLock"]

def on_key_press(e: ft.KeyboardEvent):
    if keybind_active:
        if e.key in INVALID_KEYS:
            return  # Ignore unwanted keys
        combo = []
        if e.ctrl:
            combo.append("Ctrl")
        if e.alt:
            combo.append("Alt")
        if e.shift:
            combo.append("Shift")
        combo.append(e.key)
        keybind_input.value = " + ".join(combo)
        keybind_input.update()





# ------------------------------------------------
# Function: load_song_settings
# Arguments:
#   - container: The UI container where the settings will be displayed.
#   - sound (dict): The selected sound with its properties (name, image, volume, keybind).
# Description:
#   Clears the container and displays the UI elements for editing a sound's settings:
#   name, image, volume slider, keyboard keybind input, and save button.
# ------------------------------------------------

def load_song_settings(container, sound):
    container.controls.clear()

    # Create title and sound image
    name = ft.Text(sound['name'], size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    img = ft.Image(src=sound['img'], width=200, height=200)

    # Create volume slider with label
    volume_slider = ft.Slider(
        min=0,
        max=100,
        value=sound['volume'],
        label=f"{sound['volume']}%",
        divisions=100
    )

    # Update the label when slider is moved
    def update_label(e):
        volume_slider.label = f"{int(e.control.value)}%"
        container.update()

    volume_slider.on_change = update_label

    # Set the keybind value into the input field
    keybind_input.value = sound['keybind']

    # Add all controls to the container
    container.controls.append(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [name, img],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                ft.Text("Volume"),
                volume_slider,
                ft.Text("Keyboard keybind"),
                keybind_input,
                ft.ElevatedButton(
                    text="Save",
                    on_click=lambda _: sound_manager.modify_settings_song(
                        sound['name'], volume_slider.value, keybind_input.value
                    )
                ),
            ]
        )
    )
    print("Loading page : Song Settings ")

