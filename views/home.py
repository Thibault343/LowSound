import flet as ft
import json
from modules import frontend_loader, sound_manager

delete_mode = False

# ------------------------------------------------
# Function: load_theme
# Arguments:
#   - page (ft.Page): The Flet page instance to apply the theme to.
#   - theme_name (str): Name of the theme to load.
# Description:
#   Loads the specified theme and applies it to the given page,
#   including color scheme, theme mode, and background color.
# ------------------------------------------------
def load_theme(page: ft.Page, theme_name: str):
    theme = frontend_loader.get_theme_colors(theme_name)
    page.theme = ft.Theme(color_scheme=ft.ColorScheme(**theme['color_scheme']))
    page.theme_mode = theme['theme_mode']
    page.bgcolor = theme['page_bgcolor']
    print("Theme data has been loaded.")


# ------------------------------------------------
# Function: build
# Arguments:
#   - container: The UI container where sound controls will be displayed.
#   - play_sound_fn: Callback function to play a selected sound.
#   - change_page_fn: Callback function to navigate to different pages (e.g., add sound).
# Description:
#   Builds the main sound control interface inside the given container:
#   - Clears existing UI elements.
#   - Creates a header with the title and three buttons: "Add", "Refresh", and "Delete".
#   - "Add" button triggers page change to add a new sound.
#   - "Refresh" button reloads the list of sounds.
#   - "Delete" button toggles the mode to delete sounds.
#   - Appends a placeholder column for sound buttons.
#   - Initially loads the list of sounds into the container.
# ------------------------------------------------
def build(container, play_sound_fn, change_page_fn):
    global delete_mode, delete_button

    delete_button = ft.ElevatedButton(
        text="Delete",
        on_click=lambda e: toggle_delete_mode(e, container, play_sound_fn, change_page_fn)
    )

    container.controls.clear()

    header = ft.Row(
        [
            ft.Text("Sounds", size=24, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.ElevatedButton(text="Add", data="Add", on_click=change_page_fn),
                ft.ElevatedButton(
                    text="Refresh",
                    on_click=lambda _: refresh_sounds_list(container, play_sound_fn, change_page_fn)
                ),
                delete_button,
            ])
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    container.controls.append(header)
    container.controls.append(ft.Column())  # Placeholder for sound buttons

    refresh_sounds_list(container, play_sound_fn, change_page_fn)


def delete_sound(sound, container, play_sound_fn, change_page_fn):
    sound_manager.delete_song_from_json(sound)
    refresh_sounds_list(container, play_sound_fn, change_page_fn)


# ------------------------------------------------
# Function: refresh_sounds_list
# Arguments:
#   - container: The UI container where the sounds list will be displayed.
#   - play_sound_fn: Callback function to play a selected sound.
#   - change_page_fn: Callback function to navigate to the sound settings page.
# Description:
#   Loads the list of sounds from "data/sounds.json" and updates the UI to display them.
#   - Limits the number of sounds per row to improve layout (max 7 per row).
#   - For each sound, creates a column with:
#       - An image representing the sound.
#       - A button to play the sound.
#       - A settings icon button (visible only if not in delete mode) to edit the sound.
#       - A delete icon button (visible only in delete mode) to remove the sound.
#   - Instead of replacing the control that holds the sound list,
#     it clears its children and repopulates them with the new sound rows.
#   - Calls container.update() to refresh the UI.
# ------------------------------------------------
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
                ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.colors.RED, visible=delete_mode,
                              on_click=lambda _, s=sound: delete_sound(s, container, play_sound_fn, change_page_fn)),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        rows.append(ft.Row(cols, alignment=ft.MainAxisAlignment.CENTER))

    container.controls[1] = ft.Column(rows)
    print("Refreshed page: HOME")

    if container.page:
        container.update()


# ------------------------------------------------
# Function: toggle_delete_mode
# Arguments:
#   - e: The event that triggered this function (not used directly).
#   - container: The UI container displaying the list of sounds.
#   - play_sound_fn: Callback function to play a selected sound.
#   - change_page_fn: Callback function to navigate to the sound settings page.
# Description:
#   Toggles the global delete_mode flag, which switches the UI between
#   normal mode and delete mode (showing or hiding delete buttons).
#   After toggling, it refreshes the sounds list to update the UI accordingly.
#   Also updates the delete button's style to reflect the mode.
# ------------------------------------------------
def toggle_delete_mode(e, container, play_sound_fn, change_page_fn):
    global delete_mode, delete_button
    delete_mode = not delete_mode

    if delete_mode:
        delete_button.bgcolor = ft.colors.RED_900
        delete_button.color = ft.colors.WHITE
        delete_button.text = "Delete Mode"
        print("Delete Mode ON")
    else:
        delete_button.text = "Delete"
        delete_button.bgcolor = None
        delete_button.color = None
        print("Delete Mode OFF")

    refresh_sounds_list(container, play_sound_fn, change_page_fn)
    delete_button.update()


# ------------------------------------------------
# Function: build_navbar
# Arguments:
#   - change_page_fn: Callback function to handle page navigation when a navbar item is clicked.
# Description:
#   Creates and returns a navigation bar UI component as a horizontal row,
#   containing two clickable images:
#   - A home icon ("Home") that triggers page change on tap.
#   - A settings icon ("Settings") that triggers page change on tap.
#   Each icon is wrapped in a GestureDetector to detect tap events,
#   passing the associated page name as data to the callback.
# ------------------------------------------------
def build_navbar(change_page_fn):
    return ft.Row([
        ft.GestureDetector(
            content=ft.Image(src="assets/favicon.png", width=50),
            data="Home",
            on_tap=change_page_fn
        ),
        ft.GestureDetector(
            content=ft.Image(src="assets/settings.png", width=30),
            data="Settings",
            on_tap=change_page_fn
        )
    ])
