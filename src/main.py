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

    def button_saved_device(e):
        with open('storage\data\settings.json', 'r+') as f:
            settings = json.load(f)
            settings['device'] = dropdown.value
            f.seek(0)
            json.dump(settings, f, indent=4)
            f.truncate()
    
    
    # Fonction pour jouer un son
    def play_sound(e):
        selected_sound = e.control.text
        print(f"Playing sound: {selected_sound}")
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
                    src="../assets/icon.png",  # Image pour "Paramètres"
                    width=50,
                    height=50,
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
        ft.Text("Liste des sons :"),
        *[
            ft.ElevatedButton(text=sound, on_click=play_sound)
            for sound in sounds_list
        ],
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
    settings = preloading.load_settings(dropdown)



ft.app(main)





