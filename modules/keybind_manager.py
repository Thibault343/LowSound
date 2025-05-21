from pynput import keyboard
import time
from modules import audio, sound_manager
from modules.frontend_loader import settings

sounds = sound_manager.list_sounds()
print(sounds)
current_keys = set()
last_combo = None
last_time = 0
COOLDOWN_SECONDS = 3

# ------------------------------------------------
# Function: load_keybinds
# Arguments: None
# Description:
#   Loads keybinds from the list of sounds.
#   Normalizes and sorts key combinations for consistent matching.
# Returns:
#   A dictionary mapping normalized key combinations to their corresponding sound.
# ------------------------------------------------
def load_keybinds():
    keybind_map = {}
    for sound in sounds:
        keybind = sound.get("keybind")
        if keybind:
            keys = [k.strip().title() for k in keybind.split("+")]
            key_combo = " + ".join(sorted(keys))
            keybind_map[key_combo] = sound
    return keybind_map

# ------------------------------------------------
# Function: pre_play_sound
# Arguments: combo (string)
# Description:
#   Plays the sound associated with the given key combination if it exists.
#   Uses the device and volume settings from the global settings.
# Returns:
#   None
# ------------------------------------------------
def pre_play_sound(combo):
    global settings
    keybinds = load_keybinds()
    if combo in keybinds:
        audio.play_sound(keybinds[combo]['src'], settings['device'], keybinds[combo]['volume'])

# ------------------------------------------------
# Function: normalize_key
# Arguments: key (string)
# Description:
#   Normalizes key names to ensure consistent keybind matching.
# Returns:
#   Normalized key name (string)
# ------------------------------------------------
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
current_keys = set()

# ------------------------------------------------
# Function: on_press
# Arguments: key (Key)
# Description:
#   Adds the pressed key to the current set of keys.
#   Checks if the current key combination matches any defined keybind.
# Returns:
#   None
# ------------------------------------------------
def on_press(key):
    print("PRESSED")
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

# ------------------------------------------------
# Function: on_release
# Arguments: key (Key)
# Description:
#   Removes the released key from the current set of keys.
#   Stops the listener if the Delete key is released.
# Returns:
#   False to stop the listener if Delete key is released; otherwise None
# ------------------------------------------------
def on_release(key):
    try:
        if hasattr(key, 'char') and key.char:
            k = key.char.lower()
        else:
            k = key.name.lower()
    except AttributeError:
        return
    
    if key == keyboard.Key.delete:
        print("Exiting...")
        return False

    normalized = normalize_key(k)
    current_keys.discard(normalized)
