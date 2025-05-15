import flet as ft
from modules import device, sound_manager, audio, settings_manager, frontend_loader

import json
import os

# init
devices_list = device.get_output_devices() #Get the devices list
sounds_list = sound_manager.list_sounds() # Get the sounds list
themes_list = frontend_loader.get_theme_list() # Get the  themes list
max_sounds_per_row = 7 # max button per row 

selected_song_settings = {}



# main app
def main(page: ft.Page):
    # apply settings to the app
    def apply_settings(device, theme):
        settings = frontend_loader.load_settings()
        if theme != settings["default_theme"]:
            #apply theme
            load_theme(theme)
            page.update()
            # saved settings in the json
            settings_manager.save_settings(device, theme)
        if device != settings["device"]:
            settings_manager.save_settings(device,theme)

    # load a theme
    def load_theme(theme_name) :
        if theme_name == "":
            theme = frontend_loader.get_theme_colors(None)
        else: 
            theme = frontend_loader.get_theme_colors(theme_name)
        # Convertir le dictionnaire color_scheme en ft.ColorScheme
        color_scheme = ft.ColorScheme(**theme['color_scheme'])

        # Configurer le thème de la page
        page.theme = ft.Theme(color_scheme=color_scheme)
        page.theme_mode = theme['theme_mode']
        page.bgcolor = theme['page_bgcolor']
    load_theme("")
    # Conteners pages
    home_container = ft.Column()
    settings_container = ft.Column(visible=False)
    add_song_container = ft.Column(visible=False)
    song_settings_container = ft.Column(visible=False)
    # Fonction pour gérer la sélection des pages
    def change_page(e, sound=None):
        global selected_song_settings
        target_page = e.control.data

        # Masque tous les conteneurs
        def hide_all_containers():
            home_container.visible = False
            settings_container.visible = False
            add_song_container.visible = False
            song_settings_container.visible = False

        # Affiche le conteneur demandé
        def show_container(page_name):
            global selected_song_settings
            if page_name == "Accueil":
                home_container.visible = True
                refresh_sounds_list(None)
            elif page_name == "Paramètres":
                settings_container.visible = True
            elif page_name == "Ajouter":
                add_song_container.visible = True
            elif page_name == "song_settings":
                song_settings_container.visible = True
                if sound is not None:
                        selected_song_settings = sound
                        img_path = selected_song_settings.get("img", "")  # éviter une exception si la clé n'existe pas
                        song_name_display.value = f"{selected_song_settings['name']}"
                        volume_slider.value = f"{selected_song_settings['volume']}"
                        keybind_input.value = f"{selected_song_settings['shortcut']}"
                        song_image.src = img_path  # Met à jour l’image dynamiquement
                        song_image.update()



        hide_all_containers()
        show_container(target_page)
        page.update()


    # Fonction pour jouer un son
    def play_sound(sound):
        selected_sound = sound['src']
        selected_volume = sound['volume']
        selected_device = dropdown_device.value
        audio.play_sound(selected_sound, selected_device, selected_volume)

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
        selected_song_file.update()  # Met à jour l'affichage du texte
        selected_image_file.update()

    pick_files_dialog = ft.FilePicker(
        on_result=pick_files_result
    )
    def set_status_message(msg, color):
        statuscreate.value = msg
        statuscreate.color = color
        statuscreate.update()
    
    def reset_form_fields():
        sound_name_input.value = ""
        selected_song_file.value = ""
        selected_image_file.value = ""
        sound_name_input.update()
        selected_song_file.update()
        selected_image_file.update()
    
    def on_add_song_button_click(_):
        if not sound_name_input.value.strip():
            set_status_message("Le nom du son est obligatoire.", "red")
            return
        if selected_song_file.value == "Aucun fichier sélectionné":
            set_status_message("Veuillez sélectionner un fichier audio.", "red")
            return
        sound_manager.create_new_song(sound_name_input.value, selected_song_file.value, selected_image_file.value)
        set_status_message("Son ajouté avec succès !", "green")
        reset_form_fields()


        statuscreate.update()
    # function to refresh the songs list
    def refresh_sounds_list(_):
        global sounds_list
        with open("data/sounds.json", "r") as file:
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
                                ft.IconButton(
                                    icon=ft.Icons.SETTINGS,
                                    data="song_settings",
                                    icon_size=20,
                                    visible=(not delete_mode),
                                    on_click=lambda e, s=sound: change_page(e, s),
                                    tooltip="Paramètres du son",
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
        sound_manager.delete_song_from_json(e)
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



    # ---------------------------------------------------------------------------------------------
    #                           Nav Bar
    # ---------------------------------------------------------------------------------------------
    navBar = ft.Row(
        [
            ft.GestureDetector(
                content=ft.Image(
                    src="assets/favicon.png",  # Image pour "Accueil"
                    width=70,
                    height=70,
                ),
                data="Accueil",  # Identifiant pour l'image
                on_tap=change_page,
            ),
            ft.GestureDetector(
                content=ft.Image(
                    src="assets/settings.png",  # Image pour "Paramètres"
                    width=30,
                    height=30,
                ),
                data="Paramètres",  # Identifiant pour l'image
                on_tap=change_page,
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
                        color=page.theme.color_scheme.primary,
                    ),
                ),
                # Buttons on right 
                ft.Row(
                    [
                        ft.ElevatedButton(
                            text="Ajouter",
                            data="Ajouter",
                            on_click=change_page,
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
                                    icon=ft.Icons.SETTINGS,
                                    data="song_settings",
                                    icon_size=20,
                                    visible=(not delete_mode),  # Affiche uniquement si delete_mode est False),
                                    on_click=lambda e, s=sound: change_page(e, s),
                                    tooltip="Nope",
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
    #                           Global Settings Page
    # ---------------------------------------------------------------------------------------------
        # Dropdown pour les périphériques
    dropdown_device = ft.Dropdown(
        options=[ft.dropdown.Option(device) for device in devices_list],
        autofocus=True,
    )
    dropdown_default_theme = ft.Dropdown(
        options=[ft.dropdown.Option(theme) for theme in themes_list],
        autofocus=True,
    )
    
    
    settings_container.controls = [
        ft.Text(
                    "Paramètres",
                    style=ft.TextStyle(
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color='blue',
                    ),
                ),
        ft.Text(
                    "Audio",
                    style=ft.TextStyle(
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color='blue',
                    ),
                ),
        ft.Text("Sélectionnez un périphérique audio :"),
        dropdown_device,
        ft.Text(
                    "Apparence",
                    style=ft.TextStyle(
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color='blue',
                    ),
                ),
        ft.Text("Théme:"),
        dropdown_default_theme,
        ft.ElevatedButton(text="Save", on_click=lambda _: apply_settings(dropdown_device, dropdown_default_theme)),
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
    #                           Add Song Page
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
        ft.ElevatedButton(text="Ajouter", on_click=on_add_song_button_click),
        statuscreate
    ]
    

    # ---------------------------------------------------------------------------------------------
    #                           Song Settings Page
    # ---------------------------------------------------------------------------------------------
    song_settings_title = ft.Text(
    "Song Settings",
    style=ft.TextStyle(
        size=24,
        weight=ft.FontWeight.BOLD,
        color="blue",
    ),
    text_align=ft.TextAlign.CENTER,  # Centrer le titre
    )

    # Nom de la chanson centré
    song_name_display = ft.Text(
    "Song Name Example",  # Remplace dynamiquement si nécessaire
    style=ft.TextStyle(size=30, weight=ft.FontWeight.BOLD, ),
    text_align=ft.TextAlign.CENTER,
)
    
    volume_settings_title = ft.Text(
    "Volume",
    style=ft.TextStyle(
        size=20,
    )
    )

    centered_song_name = ft.Row(
        [song_name_display],
        alignment=ft.MainAxisAlignment.CENTER
    )
    
    song_image = ft.Image(
        src="img_path",  # Remplacez par le chemin de votre image
        width=200,
        height=200,
        fit=ft.ImageFit.CONTAIN,
    )


# Définir une fonction qui met à jour le label du slider
    def update_slider_label(e):
        volume_slider.label = f'{int(volume_slider.value)}%'
        volume_slider.update()

    # Créer d'abord l'objet sans utiliser sa propre valeur dans le label
    volume_slider = ft.Slider(
        min=0,
        max=100,
        value=50,
        divisions=100,
        on_change=update_slider_label,
    ) 

    # Initialiser manuellement le label après création
    volume_slider.label = f'{int(volume_slider.value)}%'

    keybind_active = False  # Suivre si on est en mode saisie

    # Saisie clavier
    keybind_input = ft.TextField(
        label="Keybind",
        read_only=True,
        on_focus=lambda e: activate_keybind(True),
        on_blur=lambda e: activate_keybind(False),

    )
    def activate_keybind(state: bool):
        nonlocal keybind_active
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

    page.on_keyboard_event = on_key_press

    song_settings_container.controls = [
        song_settings_title,
        centered_song_name,
        ft.Row(
            controls=[song_image],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Divider(),
        volume_settings_title,
        volume_slider,
        keybind_input,
        ft.ElevatedButton(text="Save", on_click=lambda _: sound_manager.modify_settings_song(selected_song_settings['name'], volume_slider.value, keybind_input.value)),
    ]



    # ---------------------------------------------------------------------------------------------
    #                           Bottom bar
    # ---------------------------------------------------------------------------------------------
    stopAndPlayButton = ft.IconButton(
        icon=ft.Icons.STOP,
        tooltip="Arrêter",
        on_click=lambda _: audio.stop_play(),
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
                        song_settings_container,

                    ],
                    expand=True,  # Permet à cette colonne de prendre tout l'espace disponible
                ),
                bottom_bar,  # Place la barre en bas
            ],
            expand=True,  # Permet à la colonne principale de s'étendre verticalement
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Place le contenu en haut et en bas
        )
    )
    frontend_loader.load_settings_page(dropdown_device, dropdown_default_theme)
    

ft.app(main)