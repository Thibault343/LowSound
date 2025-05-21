from pynput import keyboard
import time
from sound_manager import list_sounds


sounds = list_sounds()
print(sounds)
current_keys = set()
last_combo = None
last_time = 0
COOLDOWN_SECONDS = 3
# Charge ton JSON et prépare les keybinds sous forme triée
def load_keybinds():
    keybind_map = {}

    for sound in sounds:
        keybind = sound.get("keybind")
        if keybind:
            # Normaliser et trier les touches
            keys = [k.strip().title() for k in keybind.split("+")]
            key_combo = " + ".join(sorted(keys))
            keybind_map[key_combo] = sound

    return keybind_map


def pre_play_sound(combo):
    keybinds = load_keybinds()
    if combo in keybinds:
        print(f"{combo} -> {keybinds[combo]['name']}")


# Pour normaliser les noms de touches
def normalize_key(key):
    key_map = {
        'alt_l': 'Alt',
        'alt_r': 'Alt',
        'ctrl_l': 'Ctrl',
        'ctrl_r': 'Ctrl',
        'shift': 'Shift',
        'shift_r': 'Shift',
        'cmd': 'Cmd',
        'cmd_r': 'Cmd',
    }
    return key_map.get(key.lower(), key.upper())


keybind_map = load_keybinds()
current_keys = set()  # déplacé ici pour visibilité globale


def on_press(key):
    try:
        if hasattr(key, 'char') and key.char:
            k = key.char.lower()
        else:
            k = key.name.lower()
    except AttributeError:
        return

    normalized = normalize_key(k)
    current_keys.add(normalized)

    combo = " + ".join(sorted(current_keys))
    if combo in keybind_map:
        pre_play_sound(combo)
        print(f"✅ Shortcut matched: {combo}")


def on_release(key):
    try:
        if hasattr(key, 'char') and key.char:
            k = key.char.lower()
        else:
            k = key.name.lower()
    except AttributeError:
        return

    normalized = normalize_key(k)
    current_keys.discard(normalized)

    if key == keyboard.Key.esc:
        print("Exiting...")
        return False


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()