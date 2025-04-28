import flet as ft
from scripts import api
from scripts import front_preloading as preloading
import json
import os

# init
devices_list = api.get_output_devices()
sounds_list = api.list_sounds()


def main(page: ft.Page):
    page.theme_mode = "dark"
    # Conteneurs pour les pages
    home_container = ft.Column()
    settings_container = ft.Column(visible=False)
    add_song_container = ft.Column(visible=False)

    # Fonction pour gérer la sélection des images
    def image_clicked(e):
        if e.control.data == "Accueil":
            home_container.visible = True
            settings_container.visible = False
            add_song_container.visible = False
        elif e.control.data == "Paramètres":
            home_container.visible = False
            settings_container.visible = True
            add_song_container.visible = False
        elif e.control.data == "Ajouter":
            home_container.visible = False
            settings_container.visible = False
            add_song_container.visible = True
        page.update()
    def button_add_sound_clicked(_):
        add_song_container.visible = True
        home_container.visible = False
        settings_container.visible = False
        page.update()

    def button_saved_device(_):
        with open(r'storage\data\settings.json', 'r+') as f:
            settings = json.load(f)
            settings['device'] = dropdown.value
            f.seek(0)
            json.dump(settings, f, indent=4)
            f.truncate()

    # Fonction pour jouer un son
    def play_sound(sound):
        selected_sound = sound['src']
        print(f"Playing sound: {sound['name']}")
        api.play_sound(selected_sound, dropdown.value)

    def pick_files_result(e: ft.FilePickerResultEvent):
        # Vérifiez si un fichier a été sélectionné
        if e.files and len(e.files) > 0:
            if e.files[0].path.lower().endswith(('.mp3', '.wav')):
                # Convertir le chemin absolu en chemin relatif
                selected_song_file.value = os.path.relpath(e.files[0].path, start=os.getcwd())
            else:
                # Convertir le chemin absolu en chemin relatif pour l'image
                selected_image_file.value = os.path.relpath(e.files[0].path, start=os.getcwd())
        else:
            selected_song_file.value = "Aucun fichier sélectionné"
            print("Aucun fichier sélectionné")
        selected_song_file.update()  # Met à jour l'affichage du texte
        selected_image_file.update()

    pick_files_dialog = ft.FilePicker(
        on_result=pick_files_result
    )

    def validate_and_add_song(_):
        if not sound_name_input.value.strip():
            statuscreate.value = "Le nom du son est obligatoire."
            statuscreate.color = "red"
            statuscreate.update()
            return
        if selected_song_file.value == "Aucun fichier sélectionné":
            statuscreate.value = "Veuillez sélectionner un fichier audio."
            statuscreate.color = "red"
            statuscreate.update()
            return

        # Si tout est valide, appelez la fonction pour ajouter le son
        api.createNewSong(sound_name_input.value, selected_song_file.value, selected_image_file.value)
        statuscreate.value = "Son ajouté avec succès !"
        statuscreate.color = "green"
        statuscreate.update()

    # Texte de sortie
    output_text = ft.Text()

    # Dropdown pour les périphériques
    dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(device) for device in devices_list],
        autofocus=True,
    )

    # Images dans le menu
    top_images = ft.Row(
        [
            ft.GestureDetector(
                content=ft.Image(
                    src="../assets/icon.png",  # Image pour "Accueil"
                    width=50,
                    height=50,
                ),
                data="Accueil",  # Identifiant pour l'image
                on_tap=image_clicked,
            ),
            ft.GestureDetector(
                content=ft.Image(
                    src="../assets/settings.png",  # Image pour "Paramètres"
                    width=30,
                    height=30,
                ),
                data="Paramètres",  # Identifiant pour l'image
                on_tap=image_clicked,
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    # Contenu de la page d'accueil
    home_container.controls = [
        output_text,
        ft.Row(
            [
                ft.Text(
                    "Sounds",
                    style=ft.TextStyle(
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color='blue',
                    ),
                ),
                ft.ElevatedButton(
                    text="Ajouter",
                    on_click=button_add_sound_clicked,
                    style=ft.ButtonStyle(
                        padding=ft.Padding(10, 10, 10, 10),
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        ft.Row(
            [
                ft.Column(
                    [
                        ft.Image(
                            src=sound['img'],
                            width=40,
                            height=40,
                            fit=ft.ImageFit.COVER,
                        ),
                        ft.ElevatedButton(
                            text=sound['name'], 
                            on_click=lambda _, s=sound: play_sound(s),
                            style=ft.ButtonStyle(
                                padding=ft.Padding(0, 0, 0, 0),
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
                for sound in sounds_list
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    ]

    # Contenu de la page des paramètres
    settings_container.controls = [
        ft.Text("Paramètres :"),
        ft.Text("Sélectionnez un périphérique audio :"),
        dropdown,
        ft.ElevatedButton(text="Save", on_click=button_saved_device),
        ft.Switch(label="Activer une option"),
        ft.Slider(label="Volume", min=0, max=100, value=50),
    ]

    

    selected_song_file = ft.Text(
        value="Aucun fichier sélectionné",
        style=ft.TextStyle(
            size=12,
            weight=ft.FontWeight.BOLD,
            color='blue',
        ),
    )
    selected_image_file = ft.Text(
        value="Aucune image sélectionné",
        style=ft.TextStyle(
            size=12,
            weight=ft.FontWeight.BOLD,
            color='blue',
        ),
    )

    # Ajoutez le FilePicker au page.overlay
    page.overlay.append(pick_files_dialog)

    statuscreate = ft.Text("")
    # Contenu de la page Ajouter un son
    sound_name_input = ft.TextField(label="Nom du son")
    add_song_container.controls = [
        ft.Text("Ajouter un son :"),
        sound_name_input,
        ft.Text("Sélectionner votre son :"),
        ft.ElevatedButton(
            "Sélectionner un fichier",
            icon=ft.Icons.UPLOAD_FILE,
            on_click=lambda _: pick_files_dialog.pick_files(
                allow_multiple=False,  # Limite la sélection à un seul fichier
                allowed_extensions=["mp3"]  # Autorise uniquement les fichiers audio
            ),
        ),
        selected_song_file,  # Affiche le chemin du fichier sélectionné
        ft.Text("Ajouter une image (facultatif) :"),  # Texte explicatif
        ft.ElevatedButton(
            "Sélectionner une image",
            icon=ft.Icons.UPLOAD_FILE,
            on_click=lambda _: pick_files_dialog.pick_files(
                allow_multiple=False,  # Limite la sélection à un seul fichier
                allowed_extensions=["jpg", "jpeg", "png"]  # Autorise uniquement les fichiers image
            ),
        ),
        selected_image_file,
        ft.ElevatedButton(text="Ajouter", on_click=validate_and_add_song),
        statuscreate
    ]

    

    # Mise en page principale
    page.add(
        ft.Column(
            [
                top_images,
                home_container,
                settings_container,
                add_song_container,
            ]
        )
    )
    preloading.load_settings(dropdown)

ft.app(main)





