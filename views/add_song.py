#------------------------------------------------
# Author : AkameSayte
# Date : 16 mai 2025
#------------------------------------------------
import flet as ft
from modules import sound_manager
import os

def build(container, change_page_fn):
    status_text = ft.Text()
    name_input = ft.TextField(label="Nom du son")
    song_file = ft.Text(value="Aucun fichier sélectionné")
    img_file = ft.Text(value="Aucune image sélectionnée")
    file_picker = ft.FilePicker()

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
        if not name_input.value.strip() or song_file.value == "Aucun fichier sélectionné":
            status_text.value = "Nom ou son manquant"
            return
        sound_manager.create_new_song(name_input.value, song_file.value, img_file.value)
        status_text.value = "Ajouté avec succès"
        name_input.value, song_file.value, img_file.value = "", "", "Aucun fichier sélectionné"
        container.update()

    container.controls.clear()
    container.controls.extend([
        file_picker,
        ft.Text("Ajouter un son"),
        name_input,
        ft.ElevatedButton("Choisir un fichier audio", on_click=lambda _: file_picker.pick_files(allowed_extensions=["mp3"])),
        song_file,
        ft.ElevatedButton("Choisir une image", on_click=lambda _: file_picker.pick_files(allowed_extensions=["jpg", "png", "jpeg"])),
        img_file,
        ft.ElevatedButton("Ajouter", on_click=add_song),
        status_text
    ])
