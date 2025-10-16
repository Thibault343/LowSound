import os
import json
import shutil

# ------------------------------------------------
# Function: list_sounds
# Arguments: None
# Description:
#   Attempts to load the list of available sounds from 'sounds.json'.
#   If the file is not found, returns a fallback list of default sounds.
# ------------------------------------------------
def list_sounds():
    try:
        with open("data/sounds.json", "r") as f:
            sounds = json.load(f)
            return sounds
    except FileNotFoundError:
        print("Sounds file not found. Using default sounds.")
        return ["sound1.mp3", "sound2.mp3"]


# ------------------------------------------------
# Function: delete_song_from_json
# Arguments:
#   - e (dict): A dictionary representing the sound to delete,
#               must contain 'name', 'src', and 'img' keys.
# Description:
#   Removes the specified sound from 'sounds.json' and deletes
#   its associated audio and image files from the filesystem.
#   Checks if files exist before deleting and handles exceptions.
# ------------------------------------------------
def delete_song_from_json(e):
    # Charger les sons existants
    with open("data/sounds.json", 'r') as f:
        data = json.load(f)

    # Supprimer le son correspondant
    data = [song for song in data if song['name'] != e['name']]

    # Sauvegarder la nouvelle liste
    with open("data/sounds.json", 'w') as f:
        json.dump(data, f, indent=4)

    # Supprimer les fichiers audio et image si ils existent
    for file_path in [e.get("src"), e.get("img")]:
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
            else:
                print(f"File not found, cannot delete: {file_path}")
        except Exception as err:
            print(f"Error deleting file {file_path}: {err}")

# ------------------------------------------------
# Function: create_new_song
# Arguments:
#   - songName (str): The name of the new sound.
#   - songPath (str): The file path to the audio file.
#   - imagePath (str): The file path to the image file or default if none selected.
# Description:
#   Creates a new sound entry by copying the audio and image files
#   to the designated storage folders with unique filenames to avoid overwriting.
#   Adds the new sound entry to 'sounds.json' with default volume and keybind values.
#   Handles cases where the image is not selected or filenames conflict.
# ------------------------------------------------
def create_new_song(songName, songPath, imagePath):
    # If no image is selected, use a default image
    if imagePath == "Aucune image sélectionné":
        imagePath = "assets/icon2.png"

    # If the song name is empty or contains only whitespace, do nothing and exit the function
    if songName.strip() == "":
        return

    # Extract the file extension of the audio file and convert it to lowercase
    songType = songPath.split(".")[-1].lower()

    # Define default paths for the destination audio and image files
    default_song_path = "storage/sounds/"
    dest_song_path = f"{default_song_path}{songName}.{songType}"
    dest_image_base = f"storage/images/{songName}"

    # Check if the source audio and image files exist
    src_song_file_exists = os.path.isfile(songPath)
    src_image_file_exists = os.path.isfile(imagePath)

    # Check if a destination audio file already exists to avoid overwriting
    dest_song_exists = os.path.isfile(dest_song_path)

    # If a file with the same name exists, add a numeric suffix to create a unique filename
    if dest_song_exists:
        i = 0
        while os.path.isfile(f"{default_song_path}{songName}({i}).{songType}"):
            i += 1
        songName = f"{songName}({i})"
        dest_song_path = f"{default_song_path}{songName}.{songType}"
        dest_image_base = f"storage/images/{songName}"

    # Copy the audio file from the source to the destination path
    if src_song_file_exists:
        shutil.copy2(songPath, dest_song_path)
        songPath = dest_song_path  # Update songPath to the new copied path

    # Copy the image file from the source to the destination path, ensuring the extension is valid
    if src_image_file_exists:
        image_ext = imagePath.split(".")[-1].lower()
        if image_ext not in ["png", "jpg", "jpeg"]:
            image_ext = "jpeg"  # Default to jpeg if the extension is not valid
        dest_image_path = f"{dest_image_base}.{image_ext}"
        shutil.copy2(imagePath, dest_image_path)
        imagePath = dest_image_path  # Update imagePath to the new copied path
    else:
        # If no source image found, use the default image
        imagePath = "assets/icon2.png"

    # Create a dictionary representing the new song with its properties
    new_song = {
        "name": songName,
        "src": songPath,
        "img": imagePath,
        "volume": 50,      # Default volume
        "keybind": ""     # Default empty keybind
    }

    # Load the existing list of sounds from the JSON file or create an empty list if file not found
    try:
        with open("data/sounds.json", "r") as file:
            sounds = json.load(file)
    except FileNotFoundError:
        sounds = []

    # Append the new song to the list
    sounds.append(new_song)

    # Save the updated list back to the JSON file with indentation for readability
    with open("data/sounds.json", "w") as file:
        json.dump(sounds, file, indent=4)




# ------------------------------------------------
# Function: modify_settings_song
# Arguments:
#   - name (str): The name of the sound to modify.
#   - volume (int): The new volume value (0-100).
#   - keybind (str): The new keyboard keybind for the sound.
# Description:
#   Loads the list of sounds from 'sounds.json', updates the
#   volume and keybind of the sound matching the given name,
#   then saves the updated list back to the JSON file.
#   If no matching sound is found, prints an error message.
# ------------------------------------------------
def modify_settings_song(name, volume, keybind):
    with open("data/sounds.json", "r") as f:
        sounds = json.load(f)

    for sound in sounds:
        if sound["name"] == name:
            sound["volume"] = volume
            sound["keybind"] = keybind
            break
    else:
        print(f"❌ Aucun son trouvé avec le nom : {name}")
        return

    with open("data/sounds.json", "w") as f:
        json.dump(sounds, f, indent=4)

    print(f"✅ Data of {name} updated")
