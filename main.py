import flet as ft
from views import home, settings, add_song, song_settings
from modules import frontend_loader, settings_manager, device, sound_manager

def main(page: ft.Page):
    # Initial setup
    page.title = "Soundboard"
    page.window_width = 1000
    page.window_height = 700
    page.window_resizable = True

    # Load saved settings
    settings_data = frontend_loader.load_settings()
    devices_list = device.get_output_devices()
    themes_list = frontend_loader.get_theme_list()

    # Apply theme
    home.load_theme(page, settings_data["default_theme"])

    # Page containers
    home_container = ft.Column(visible=True)
    settings_container = ft.Column(visible=False)
    add_song_container = ft.Column(visible=False)
    song_settings_container = ft.Column(visible=False)

    containers = {
        "Accueil": home_container,
        "Paramètres": settings_container,
        "Ajouter": add_song_container,
        "song_settings": song_settings_container
    }

    def change_page(e, sound=None):
        # Hide all
        for container in containers.values():
            container.visible = False

        # Show selected
        containers[e.control.data].visible = True
        if e.control.data == "Accueil":
            home.refresh_sounds_list(home_container, play_sound, change_page)
        elif e.control.data == "song_settings":
            song_settings.load_song_settings(song_settings_container, sound)

        page.update()

    def play_sound(sound):
        from modules import audio
        audio.play_sound(sound['src'], settings_data["device"], sound['volume'])

    
    page.on_keyboard_event = song_settings.on_key_press

    # Build each page
    home.build(home_container, play_sound, change_page)
    settings.build(settings_container, devices_list, themes_list, lambda d, t: apply_settings(d, t, page))
    add_song.build(add_song_container, change_page)

    def apply_settings(device_val, theme_val, page):
        settings_manager.save_settings(device_val, theme_val)
        home.load_theme(page, theme_val)

    # Navigation bar
    navbar = home.build_navbar(change_page)

    # Add all controls to the page
    page.add(navbar, home_container, settings_container, add_song_container, song_settings_container)

    # Maintenant que le container est bien dans la page, on peut appeler refresh
    home.refresh_sounds_list(home_container, play_sound, change_page)

ft.app(target=main)
