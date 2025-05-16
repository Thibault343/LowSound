
#   <--|========>


import flet as ft
from modules import sound_manager

#------------------------------------------------
#   **     keybind input management     **
# - Autodetect and select mode when a user can select a shortcut
# - limit the shortcut possiblity
#------------------------------------------------

keybind_active = False

keybind_input = ft.TextField(
    label="Keybind",
    read_only=True,
    on_focus=lambda e: activate_keybind(True),
    on_blur=lambda e: activate_keybind(False),

)

def activate_keybind(state: bool):
    global keybind_active
    keybind_active = state
    if state:
        keybind_input.value = "Press a key..."
    else:
        if keybind_input.value == "Press a key...":
            keybind_input.value = ""
    keybind_input.update()


def on_key_press(e: ft.KeyboardEvent):
    if keybind_active:
        # On peut construire la combinaison de touches ici
        combo = []
        if e.ctrl:
            combo.append("Ctrl")
        if e.alt:
            combo.append("Alt")
        if e.shift:
            combo.append("Shift")
        combo.append(e.key)  # Ajoute la touche principale
        keybind_input.value = " + ".join(combo)
        keybind_input.update()

#------------------------------------------------
#   **     Load song settings     **
# Arguments Taked: container and the actualy selected sound
# DO :  - Create title and use sounds settings to add the song name,
#       - Create a image with src the sound image
#------------------------------------------------

def load_song_settings(container, sound):
    container.controls.clear()
    print(sound)
    name = ft.Text(sound['name'], size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    img = ft.Image(src=sound['img'], width=200, height=200)

    volume_slider = ft.Slider(min=0, max=100, value=sound['volume'], label=f"{sound['volume']}%", divisions=100)
    keybind_input.value = f'{sound['shortcut']}'

    # Saisie clavier



    container.controls.clear()
    
    def update_label(e):
        volume_slider.label = f"{int(e.control.value)}%"
        container.update()
    


    volume_slider.on_change = update_label
    container.controls.append(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                name,
                                img
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                ft.Text("Volume"),
                volume_slider,
                ft.Text("Raccourci clavier"),
                keybind_input,
                ft.ElevatedButton(text="Save", on_click=lambda _: sound_manager.modify_settings_song(sound['name'], volume_slider.value, keybind_input.value)),
            ],
        )
    )
