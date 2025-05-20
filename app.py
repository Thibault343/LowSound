import flet as ft
from views import home, settings, add_song, song_settings
from modules import frontend_loader, settings_manager, device, sound_manager, audio

def main(page: ft.Page):
    # Window configuration
    page.title = "Soundboard"
    page.window_width = 1000
    page.window_height = 700
    page.window_resizable = True

    # Load saved settings
    settings_data = frontend_loader.load_settings()
    devices_list = device.get_output_devices()
    themes_list = frontend_loader.get_theme_list()

    # Apply selected theme
    home.load_theme(page, settings_data["default_theme"])

    # Page containers
    home_container = ft.Column(visible=True)
    settings_container = ft.Column(visible=False)
    add_song_container = ft.Column(visible=False)
    song_settings_container = ft.Column(visible=False)

    containers = {
        "Home": home_container,
        "Settings": settings_container,
        "Add": add_song_container,
        "song_settings": song_settings_container
    }

    def change_page(e, sound=None):
        # Hide all pages
        for container in containers.values():
            container.visible = False

        # Show selected page
        containers[e.control.data].visible = True

        if e.control.data == "Home":
            home.refresh_sounds_list(home_container, play_sound, change_page)
        elif e.control.data == "song_settings":
            song_settings.load_song_settings(song_settings_container, sound)

        page.update()

    def play_sound(sound):
        audio.play_sound(sound['src'], settings_data["device"], sound['volume'])

    def apply_settings(device_val, theme_val, page):
        settings_manager.save_settings(device_val, theme_val)
        home.load_theme(page, theme_val)

    # ------------------------------------------------
    # Function: on_key_press
    # Arguments:
    #   - e (ft.KeyboardEvent): The keyboard event triggered by a key press.
    # Description:
    #   If keybind input mode is active, constructs and displays the key combination
    #   (e.g., Ctrl + Shift + A) based on the pressed keys.
    # ------------------------------------------------
    page.on_keyboard_event = song_settings.on_key_press

    # Build all views
    home.build(home_container, play_sound, change_page)
    settings.build(settings_container, devices_list, themes_list, lambda d, t: apply_settings(d, t, page))
    add_song.build(add_song_container, change_page)

    # Navigation bar
    navbar = home.build_navbar(change_page)

    # Bottom bar with Stop button
    bottom_bar = ft.Container(
        content=ft.Row(
            [ft.IconButton(
                icon=ft.Icons.STOP,
                tooltip="Stop",
                on_click=lambda _: audio.stop_play()
            )],
            alignment=ft.MainAxisAlignment.END,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        height=50,
        bgcolor="lightgray",
        padding=ft.Padding(10, 0, 10, 0),
    )

    # Layout structure
    page.add(
        ft.Column(
            [
                ft.Column(
                    [
                        navbar,
                        home_container,
                        settings_container,
                        add_song_container,
                        song_settings_container,
                    ],
                    expand=True
                ),
                bottom_bar
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    )

    # Initial refresh of the home view
    home.refresh_sounds_list(home_container, play_sound, change_page)

ft.app(target=main)