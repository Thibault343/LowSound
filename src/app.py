import flet as ft
from scripts import api
from scripts import front_preloading as preloading
import json

# init
devices_list = api.get_output_devices()
sounds_list = api.list_sounds()





def main(page: ft.Page):
    # Conteneurs pour les pages
    home_container = ft.Column()
    settings_container = ft.Column(visible=False)

    # Fonction pour gérer la sélection des images
    def image_clicked(e):
        if e.control.data == "Accueil":
            home_container.visible = True
            settings_container.visible = False
        elif e.control.data == "Paramètres":
            home_container.visible = False
            settings_container.visible = True
        page.update()

    def button_saved_device():
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
        ft.Text(
            "Sounds",
            style=ft.TextStyle(
                size=24,
                weight=ft.FontWeight.BOLD,
                color='blue',
            ),
        ),
        ft.Row(  # Utilisation de ft.Row pour aligner les boutons horizontalement
            [
                ft.Column(
                    [
                        ft.Image(
                            src=sound['img'],  # Utilisation de sound['src'] pour le chemin de l'image
                            width=40,
                            height=40,
                            fit=ft.ImageFit.COVER,
                        ),
                        ft.ElevatedButton(
                            text=sound['name'], 
                            on_click=lambda e, s=sound: play_sound(s),
                            style=ft.ButtonStyle(
                                padding=ft.Padding(0, 0, 0, 0),  # Corrected Padding usage
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  # Centrer les images et boutons verticalement
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrer horizontalement
                )
                for sound in sounds_list
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centrer les colonnes horizontalement dans la rangée
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

    # Mise en page principale
    page.add(
        ft.Column(
            [
                top_images,
                home_container,
                settings_container,
            ]
        )
    )
    preloading.load_settings(dropdown)



ft.app(main)





