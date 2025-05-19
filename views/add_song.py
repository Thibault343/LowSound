import flet as ft
from modules import sound_manager
import os

# ------------------------------------------------
# Function: build
# Arguments:
#   - container: The UI container where the elements will be added.
#   - change_page_fn: Callback function to handle page changes.
# Description:
#   Builds the UI for adding a new sound, including:
#   - A status text placeholder.
#   - A text field for entering the sound's name.
#   - Text fields displaying the selected song file and image file paths.
#   - A file picker component to select audio (.mp3) and image (.jpg, .png, .jpeg) files.
#   When a file is picked, updates the corresponding text fields with the relative file path.
# ------------------------------------------------
def build(container, change_page_fn):
    status_text = ft.Text()
    name_input = ft.TextField(label="Sound name")
    song_file = ft.Text(value="No file selected")
    img_file = ft.Text(value="No image selected")
    file_picker = ft.FilePicker()
    print("Loading page : Add song ")

    def on_file_pick(e: ft.FilePickerResultEvent):
        if e.files:
            path = e.files[0].path
            if path.endswith(".mp3"):
                song_file.value = os.path.relpath(path)
            elif path.endswith((".jpg", ".png", ".jpeg")):
                img_file.value = os.path.relpath(path)
        container.update()

    file_picker.on_result = on_file_pick

    def add_song(_):
        if not name_input.value.strip() or song_file.value == "No file selected":
            status_text.value = "Missing name or sound file"
            status_text.color = "red"
            return
        sound_manager.create_new_song(name_input.value, song_file.value, img_file.value)
        status_text.value = "Successfully added"
        status_text.color = "green"
        name_input.value, song_file.value, img_file.value = "", "No file selected", "No image selected"
        container.update()
    
    container.controls.clear()
    container.controls.extend([
        file_picker,
        ft.Text("Add a sound"),
        name_input,
        ft.ElevatedButton("Choose an audio file", on_click=lambda _: file_picker.pick_files(allowed_extensions=["mp3"])),
        song_file,
        ft.ElevatedButton("Choose an image", on_click=lambda _: file_picker.pick_files(allowed_extensions=["jpg", "png", "jpeg"])),
        img_file,
        ft.ElevatedButton("Add", on_click=add_song),
        status_text
    ])
    
