import sounddevice as sd
import soundfile as sf
import shutil
import json
import os

def get_output_devices():
    """
    Retourne une liste des noms de périphériques audio de sortie disponibles.
    """
    devices = sd.query_devices()
    output_devices = [d['name'] for d in devices if d['max_output_channels'] > 0]
    return output_devices
    
def list_sounds():
    """
    Retourne une liste des fichiers .wav dans le dossier des sons.
    """
    try:
        with open("storage\data\sounds.json", "r") as f:
            sounds = json.load(f)
            return sounds
    except FileNotFoundError:
        print("Sounds file not found. Using default sounds.")
        return ["sound1.mp3", "sound2.mp3"]

def saved_settings(dd):
    with open(r'storage\data\settings.json', 'r+') as f:
        settings = json.load(f)
        settings['device'] = dd.value
        f.seek(0)
        json.dump(settings, f, indent=4)
        f.truncate()

def delete_song_from_json(e):
    print(e)
    with open("storage/data/sounds.json", 'r') as f:
        data = json.load(f)

    # Supprimer la chanson avec le nom correspondant
    data = [song for song in data if song['name'] != e['name']]

    # Écrire les données mises à jour dans le fichier JSON
    with open("storage/data/sounds.json", 'w') as f:
        json.dump(data, f, indent=4)
    os.remove(e["src"])
    
    

def play_sound(sound, selected_device):
    # Utiliser directement le nom du périphérique sélectionné
    device_name = selected_device  # selected_device est déjà une chaîne
    device_info = next((d for d in sd.query_devices() if d['name'] == device_name), None)
    if device_info:
        try:
            file_path = f"./{sound}"
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


def createNewSong(songName, songPath, imagePath):
    if imagePath == "Aucune image sélectionné": # Si l'image n'est pas spécifiée, on utilise une image par défaut
        imagePath = "../assets/icon2.png"
    
    if songName.replace(" ", "") != "":
        shutil.copy2(songPath, f"storage/data/sounds/{songName}.mp3")  # Copie le fichier audio dans le dossier de stockage
        songPath = f"storage/data/sounds/{songName}.mp3"  # Met à jour le chemin du fichier audio
        new_song = {
            "name": songName,
            "src": songPath if songPath.replace(" ", "") != "" else "",
            "img": imagePath if imagePath.replace(" ", "") != "" else "../assets/icon2.png"
        }
        try:
            with open("storage/data/sounds.json", "r") as file:
                sounds = json.load(file)
        except FileNotFoundError:
            sounds = []  # Initialize an empty list if the file doesn't exist
        
        sounds.append(new_song)
        with open("storage/data/sounds.json", "w") as file:
            json.dump(sounds, file, indent=4)
        
            



    

                

if __name__ == "__main__":
    main()
