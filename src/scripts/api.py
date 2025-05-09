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

<<<<<<< Updated upstream

def createNewSong(songName, songPath, imagePath):
    if imagePath == "Aucune image sélectionné": # Si l'image n'est pas spécifiée, on utilise une image par défaut
        imagePath = "../assets/icon2.png"
    
    if songName.replace(" ", "") != "":
        shutil.copy2(songPath, f"storage/data/sounds/{songName}.mp3")  # Copie le fichier audio dans le dossier de stockage
        songPath = f"storage/data/sounds/{songName}.mp3"  # Met à jour le chemin du fichier audio
=======
# Create and save a new song entry (copy audio/image files, update JSON)
import os
import shutil
import json

def createNewSong(songName, songPath, imagePath):
    # Use default image if none selected
    if imagePath == "Aucune image sélectionné":
        imagePath = "../assets/icon2.png"

    # Proceed only if the song name is not empty or just spaces
    if songName.strip() != "":
        # Get the song file extension
        songType = songPath.split(".")[-1].lower()

        # Destination paths
        dest_song_path = f"storage/data/sounds/{songName}.{songType}"
        dest_image_base = f"storage/data/images/{songName}"

        # Check if source files exist
        song_file_exists = os.path.isfile(songPath)
        image_file_exists = os.path.isfile(imagePath)

        # Copy song if valid
        if song_file_exists:
            shutil.copy2(songPath, dest_song_path)
            songPath = dest_song_path  # Update to new location

        # Copy image if valid and set appropriate extension
        if image_file_exists:
            image_ext = imagePath.split(".")[-1].lower()
            if image_ext in ["png", "jpg", "jpeg"]:
                dest_image_path = f"{dest_image_base}.{image_ext}"
            else:
                dest_image_path = f"{dest_image_base}.jpeg"  # Default to .jpeg

            shutil.copy2(imagePath, dest_image_path)
            imagePath = dest_image_path  # Update to new location
        else:
            imagePath = "../assets/icon2.png"  # Default image if not found

        # Create the new song entry
>>>>>>> Stashed changes
        new_song = {
            "name": songName,
            "src": songPath if os.path.isfile(songPath) else "",
            "img": imagePath if os.path.isfile(imagePath) else "../assets/icon2.png"
        }
<<<<<<< Updated upstream
=======

        # Read existing songs and append the new one
>>>>>>> Stashed changes
        try:
            with open("storage/data/sounds.json", "r") as file:
                sounds = json.load(file)
        except FileNotFoundError:
<<<<<<< Updated upstream
            sounds = []  # Initialize an empty list if the file doesn't exist
        
=======
            sounds = []  # Start with empty list if file does not exist

>>>>>>> Stashed changes
        sounds.append(new_song)

        # Write updated list back to the file
        with open("storage/data/sounds.json", "w") as file:
            json.dump(sounds, file, indent=4)
        
            



    

                

<<<<<<< Updated upstream
=======

# Run the main function if script is executed directly
>>>>>>> Stashed changes
if __name__ == "__main__":
    main()
