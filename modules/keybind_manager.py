from pynput import keyboard
import time


current_keys = set()
last_combo = None
last_time = 0
COOLDOWN_SECONDS = 3
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

def on_press(key):
    global last_combo, last_time

    try:
        if hasattr(key, 'char') and key.char:
            k = key.char.lower()
        else:
            k = key.name.lower()
    except AttributeError:
        return

    current_keys.add(normalize_key(k))

    combo = ' + '.join(sorted(current_keys))

    now = time.time()
    if combo == last_combo and now - last_time < COOLDOWN_SECONDS:
        # Ignorer si même combo dans les 3 sec
        return

    last_combo = combo
    last_time = now

    print(f"Shortcut detected: {combo}")

def on_release(key):
    try:
        if hasattr(key, 'char') and key.char:
            k = key.char.lower()
        else:
            k = key.name.lower()
    except AttributeError:
        return

    current_keys.discard(normalize_key(k))

    if key == keyboard.Key.esc:
        print("Exiting...")
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()