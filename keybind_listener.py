from pynput import keyboard
from modules import keybind_manager

if __name__ == "__main__":
    with keyboard.Listener(on_press=keybind_manager.on_press, on_release=keybind_manager.on_release) as listener:
        listener.join()
