import sounddevice as sd
import soundfile as sf
from os import listdir

def get_output_devices():
    """
    Retourne une liste des noms de périphériques audio de sortie disponibles.
    """
    devices = sd.query_devices()
    output_devices = [d['name'] for d in devices if d['max_output_channels'] > 0]
    return output_devices

def list_sounds(directory="./sounds"):
    """
    Retourne une liste des fichiers .wav dans le dossier des sons.
    """
    try:
        files = listdir(directory)
        sounds = [f for f in files if f.endswith(".mp3")]
        return sounds
    except FileNotFoundError:
        print(f"Dossier '{directory}' non trouvé.")
        return []

def play_sound(sound, selected_device):
    # Utiliser directement le nom du périphérique sélectionné
    device_name = selected_device  # selected_device est déjà une chaîne
    device_info = next((d for d in sd.query_devices() if d['name'] == device_name), None)
    if device_info:
        try:
            file_path = f"./sounds/{sound}"
            data, samplerate = sf.read(file_path)
            sd.play(data, samplerate=samplerate, device=device_info['name'])
        except Exception as e:
            print(f"Error playing sound: {e}")
    else:
        print("Selected device not found.")

def main():
    print("🔊 Recherche des périphériques audio de sortie...")
    output_devices = get_output_devices()
    
    if not output_devices:
        print("❌ Aucun périphérique de sortie audio détecté.")
    else:
        print("✅ Périphériques détectés :")
        for i, dev in enumerate(output_devices):
            print(f"{i + 1}. {dev}")
    
    return output_devices

if __name__ == "__main__":
    main()
