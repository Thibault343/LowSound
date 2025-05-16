#------------------------------------------------
# Author : AkameSayte
# Date : 16 mai 2025
#------------------------------------------------
import flet as ft
from modules import frontend_loader


def build(container, devices, themes, on_save):
    settings = frontend_loader.load_settings()
    print(settings)
    dropdown_device = ft.Dropdown(options=[ft.dropdown.Option(d) for d in devices], value=settings['device'])
    dropdown_theme = ft.Dropdown(options=[ft.dropdown.Option(t) for t in themes], value=settings['default_theme'])

    container.controls.clear()
    container.controls.extend([
        ft.Text("Paramètres", size=24, weight=ft.FontWeight.BOLD),
        ft.Text("Périphérique audio :"),
        dropdown_device,
        ft.Text("Thème :"),
        dropdown_theme,
        ft.ElevatedButton(text="Enregistrer", on_click=lambda _: on_save(dropdown_device.value, dropdown_theme.value))
    ])
