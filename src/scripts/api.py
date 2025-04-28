import sounddevice as sd
import soundfile as sf
from os import listdir
import shutil
import json
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
    if imagePath == "Aucune image sélectionné":
        imagePath = ""
    if songName.strip() != "":
        new_song = {"name": songName}
        
        if songPath.strip() != "":
            shutil.copy(songPath, "../sounds")
            new_song["src"] = songPath
            
            if imagePath.strip() == "":
                # Load default image
                new_song["img"] = "../assets/icon2.png"
            else:
                new_song["img"] = imagePath
        
        try:
            # Load existing data
            with open("storage\\data\\sounds.json", "r") as file:
                sounds = json.load(file)
        except FileNotFoundError:
            # If file doesn't exist, start with an empty list
            sounds = []
        
        # Append the new song to the list
        sounds.append(new_song)
        
        # Save the updated list back to the file
        with open("storage\\data\\sounds.json", "w") as file:
            json.dump(sounds, file, indent=4)


    

                

if __name__ == "__main__":
    main()
