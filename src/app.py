import flet as ft
from scripts import api
from scripts.api import delete_song_from_json
from scripts.api import saved_settings
from scripts.api import pause_and_play
from scripts import front_preloading as preloading
import json
import os

# init
devices_list = api.get_output_devices()
sounds_list = api.list_sounds()
max_sounds_per_row = 7


def main(page: ft.Page):
    page.theme_mode = "dark"
    # Conteneurs pour les pages
    home_container = ft.Column()
    settings_container = ft.Column(visible=False)
    add_song_container = ft.Column(visible=False)

    # Fonction pour gérer la sélection des pages
    def change_Page(e):
        if e.control.data == "Accueil":
            home_container.visible = True
            settings_container.visible = False
            add_song_container.visible = False
            refresh_sounds_list(None)  # Met à jour la liste des sons
        elif e.control.data == "Paramètres":
            home_container.visible = False
            settings_container.visible = True
            add_song_container.visible = False
        elif e.control.text == "Ajouter":
            home_container.visible = False
            settings_container.visible = False
            add_song_container.visible = True
        page.update()

    # Fonction pour jouer un son
    def play_sound(sound):
        selected_sound = sound['src']
        print(f"Playing sound: {sound['name']}")
        api.play_sound(selected_sound, dropdown.value)

    # Fuction to pick a file
    def pick_files_result(e: ft.FilePickerResultEvent):
        # Vérifiez si un fichier a été sélectionné
        if e.files and len(e.files) > 0:
            if e.files[0].path.lower().endswith(('.mp3', '.wav')):
                # Convertir le chemin absolu en chemin relatif
                if os.path.splitdrive(e.files[0].path)[0] == os.path.splitdrive(os.getcwd())[0]:
                    selected_song_file.value = os.path.relpath(e.files[0].path, start=os.getcwd())
                else:
                    selected_song_file.value = e.files[0].path
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
    # function if a song is available to be create
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
        sound_name_input.value = ""
        selected_song_file.value = ""
        selected_image_file.value = ""
        sound_name_input.update()
        selected_song_file.update()
        selected_image_file.update()

        statuscreate.update()
    # function to refresh the songs list
    def refresh_sounds_list(_):
        global sounds_list
        with open("storage/data/sounds.json", "r") as file:
            sounds_list = json.load(file)
        sounds_list = [sound for sound in sounds_list if sound['src'] != ""]  # Filtrer les sons sans chemin valide

        # Mettre à jour la liste des sons
        home_container.controls[1] = ft.Column(
            [
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
                                # Bouton corbeille visible uniquement en mode suppression
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color=ft.Colors.RED,
                                    on_click=lambda _, s=sound: delete_songs(s),
                                    visible=delete_mode,  # Affiche uniquement si delete_mode est True
                                ),

                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        )
                        for sound in sounds_list[row_start:row_start + max_sounds_per_row]
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
                for row_start in range(0, len(sounds_list), max_sounds_per_row)
            ]
        )
        page.update()

    # Setup delete function
    delete_mode = False
    def delete_songs(e) :
        delete_song_from_json(e)
        page.update()
        refresh_sounds_list(None)  # Met à jour la liste des sons
    
    def toggle_delete_mode(e):
        nonlocal delete_mode
        delete_mode = not delete_mode  # Inverse l'état du mode suppression
        if delete_mode:
            e.control.style.bgcolor = 'red'
            e.control.style.color = 'white'  # Change la couleur du texte en blanc
        else:
            e.control.style.bgcolor = None
            e.control.style.color = None  # Réinitialise la couleur du texte

        page.update()
        refresh_sounds_list(None)  # Met à jour la liste des sons

    # Dropdown pour les périphériques
    dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(device) for device in devices_list],
        autofocus=True,
    )

    # ---------------------------------------------------------------------------------------------
    #                           Nav Bar
    # ---------------------------------------------------------------------------------------------
    navBar = ft.Row(
        [
            ft.GestureDetector(
                content=ft.Image(
                    src="../assets/icon.png",  # Image pour "Accueil"
                    width=50,
                    height=50,
                ),
                data="Accueil",  # Identifiant pour l'image
                on_tap=change_Page,
            ),
            ft.GestureDetector(
                content=ft.Image(
                    src="../assets/settings.png",  # Image pour "Paramètres"
                    width=30,
                    height=30,
                ),
                data="Paramètres",  # Identifiant pour l'image
                on_tap=change_Page,
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
    )
    
    # ---------------------------------------------------------------------------------------------
    #                           Home Page
    # ---------------------------------------------------------------------------------------------
    home_container.controls = [
        ft.Row(
            [
                # Sounds Title
                ft.Text(
                    "Sounds",
                    style=ft.TextStyle(
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color='blue',
                    ),
                ),
                # Buttons on right 
                ft.Row(
                    [
                        ft.ElevatedButton(
                            text="Ajouter",
                            on_click=change_Page,
                            style=ft.ButtonStyle(
                                padding=ft.Padding(10, 10, 10, 10),
                            ),
                        ),
                        ft.ElevatedButton(
                            text="Refresh",
                            on_click=refresh_sounds_list,
                            style=ft.ButtonStyle(
                                padding=ft.Padding(10, 10, 10, 10),
                            ),
                        ),
                        ft.ElevatedButton(
                            text="Supprimer",
                            on_click=toggle_delete_mode,
                            style=ft.ButtonStyle(
                                padding=ft.Padding(10, 10, 10, 10),
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        # Generated boutons
        ft.Column(
            [
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
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color=ft.Colors.PINK_700,
                                    icon_size=20,
                                    tooltip="Nope",
                                    visible= delete_mode,
                                    on_click=delete_songs,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        )
                        for sound in sounds_list[row_start:row_start + max_sounds_per_row]
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
                for row_start in range(0, len(sounds_list), max_sounds_per_row)
            ]
        ),
    ]

    # ---------------------------------------------------------------------------------------------
    #                           Settings Page
    # ---------------------------------------------------------------------------------------------
    settings_container.controls = [
        ft.Text(
                    "Paramêtre",
                    style=ft.TextStyle(
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color='blue',
                    ),
                ),
        ft.Text("Sélectionnez un périphérique audio :"),
dropdown,
ft.ElevatedButton(text="Save", on_click=lambda _: saved_settings(dropdown)),
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


    # ---------------------------------------------------------------------------------------------
    #                           Add song Page
    # ---------------------------------------------------------------------------------------------
    statuscreate = ft.Text("")
    # Contenu de la page Ajouter un son
    sound_name_input = ft.TextField(label="Nom du son")

    add_song_container.controls = [
        ft.Text("Ajouter un son :"),
        sound_name_input,
        ft.Text("Sélectionner votre son :"),
        ft.ElevatedButton(
            "Sélectionner un fichier",
            on_click=lambda _: pick_files_dialog.pick_files(
                allow_multiple=False,  # Limite la sélection à un seul fichier
                allowed_extensions=["mp3"]  # Autorise uniquement les fichiers audio
            ),
        ),
        selected_song_file,  # Affiche le chemin du fichier sélectionné
        ft.Text("Ajouter une image (facultatif) :"),  # Texte explicatif
        ft.ElevatedButton(
            "Sélectionner une image",
            on_click=lambda _: pick_files_dialog.pick_files(
                allow_multiple=False,  # Limite la sélection à un seul fichier
                allowed_extensions=["jpg", "jpeg", "png"]  # Autorise uniquement les fichiers image
            ),
        ),
        selected_image_file,
        ft.ElevatedButton(text="Ajouter", on_click=validate_and_add_song),
        statuscreate
    ]
    stopAndPlayButton = ft.IconButton(
        icon=ft.Icons.STOP,
        tooltip="Arrêter",
        on_click=lambda _: pause_and_play(),
    )

    # Barre en bas avec les boutons Arrêter et Pause
    bottom_bar = ft.Container(
        content=ft.Row(
            [
                stopAndPlayButton,
            ],
            alignment=ft.MainAxisAlignment.END,  # Aligne les boutons à droite
            vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Centre les boutons verticalement
        ),
        height=50,  # Hauteur de la barre
        bgcolor="lightgray",  # Couleur de fond
        padding=ft.Padding(10, 0, 10, 0),  # Ajoute un peu de marge sur les côtés
    )

    # Mise en page principale
    page.add(
        ft.Column(
            [
                ft.Column(
                    [
                        navBar,
                        home_container,
                        settings_container,
                        add_song_container,
                    ],
                    expand=True,  # Permet à cette colonne de prendre tout l'espace disponible
                ),
                bottom_bar,  # Place la barre en bas
            ],
            expand=True,  # Permet à la colonne principale de s'étendre verticalement
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Place le contenu en haut et en bas
        )
    )
    preloading.load_settings(dropdown)

ft.app(main)





