#------------------------------------------------
# Author : AkameSayte
# Date : 16 mai 2025
#------------------------------------------------

import flet as ft
import json
from modules import frontend_loader, sound_manager

delete_mode = False

def load_theme(page: ft.Page, theme_name: str):
    theme = frontend_loader.get_theme_colors(theme_name)
    page.theme = ft.Theme(color_scheme=ft.ColorScheme(**theme['color_scheme']))
    page.theme_mode = theme['theme_mode']
    page.bgcolor = theme['page_bgcolor']

def build(container, play_sound_fn, change_page_fn):
    global delete_mode
    container.controls.clear()

    header = ft.Row(
        [
            ft.Text("Sounds", size=24, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.ElevatedButton(text="Ajouter", data="Ajouter", on_click=change_page_fn),
                ft.ElevatedButton(text="Refresh", on_click=lambda _: refresh_sounds_list(container, play_sound_fn, change_page_fn)),
                ft.ElevatedButton(text="Supprimer", on_click=lambda e: toggle_delete_mode(e, container, play_sound_fn, change_page_fn)),
            ])
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    container.controls.append(header)
    container.controls.append(ft.Column())  # Placeholder pour les boutons

    # Ne pas faire container.update() ici si container n’est pas encore affiché
    refresh_sounds_list(container, play_sound_fn, change_page_fn)  # Chargement initial des sons
    # container.update()  # Mise à jour de l'interface


def refresh_sounds_list(container, play_sound_fn, change_page_fn):
    global delete_mode
    max_sounds_per_row = 7
    with open("data/sounds.json", "r") as f:
        sounds = json.load(f)
    sounds = [s for s in sounds if s['src']]

    rows = []
    for row_start in range(0, len(sounds), max_sounds_per_row):
        cols = []
        for sound in sounds[row_start:row_start + max_sounds_per_row]:
            cols.append(ft.Column([
                ft.Image(src=sound['img'], width=40, height=40),
                ft.ElevatedButton(text=sound['name'], on_click=lambda _, s=sound: play_sound_fn(s)),
                ft.IconButton(icon=ft.Icons.SETTINGS, data="song_settings", visible=not delete_mode,
                              on_click=lambda e, s=sound: change_page_fn(e, s)),
                ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED, visible=delete_mode,
                              on_click=lambda _, s=sound: sound_manager.delete_song_from_json(s)),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        rows.append(ft.Row(cols, alignment=ft.MainAxisAlignment.CENTER))

    container.controls[1] = ft.Column(rows)

def toggle_delete_mode(e, container, play_sound_fn, change_page_fn):
    global delete_mode
    delete_mode = not delete_mode
    refresh_sounds_list(container, play_sound_fn, change_page_fn)

def build_navbar(change_page_fn):
    return ft.Row([
        ft.GestureDetector(
            content=ft.Image(src="assets/favicon.png", width=50),
            data="Accueil",
            on_tap=change_page_fn
        ),
        ft.GestureDetector(
            content=ft.Image(src="assets/settings.png", width=30),
            data="Paramètres",
            on_tap=change_page_fn
        )
    ])
