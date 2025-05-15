import os
import json
import shutil

def list_sounds():
    """
    Returns a list of .wav files from the sound folder.
    """
    try:
        with open("data/sounds.json", "r") as f:
            sounds = json.load(f)
            return sounds
    except FileNotFoundError:
        print("Sounds file not found. Using default sounds.")
        return ["sound1.mp3", "sound2.mp3"]

def delete_song_from_json(e):
    with open("data/sounds.json", 'r') as f:
        data = json.load(f)

    data = [song for song in data if song['name'] != e['name']]

    with open("data/sounds.json", 'w') as f:
        json.dump(data, f, indent=4)

    os.remove(e["src"])
    os.remove(e["img"])

def create_new_song(songName, songPath, imagePath):
    if imagePath == "Aucune image sélectionné":
        imagePath = "assets/icon2.png"

    if songName.strip() == "":
        return

    songType = songPath.split(".")[-1].lower()
    default_song_path = "storage/sounds/"
    dest_song_path = f"{default_song_path}{songName}.{songType}"
    dest_image_base = f"storage/images/{songName}"

    src_song_file_exists = os.path.isfile(songPath)
    src_image_file_exists = os.path.isfile(imagePath)
    dest_song_exists = os.path.isfile(dest_song_path)

    if dest_song_exists:
        i = 0
        while os.path.isfile(f"{default_song_path}{songName}({i}).{songType}"):
            i += 1
        songName = f"{songName}({i})"
        dest_song_path = f"{default_song_path}{songName}.{songType}"
        dest_image_base = f"storage/images/{songName}"

    if src_song_file_exists:
        shutil.copy2(songPath, dest_song_path)
        songPath = dest_song_path

    if src_image_file_exists:
        image_ext = imagePath.split(".")[-1].lower()
        if image_ext not in ["png", "jpg", "jpeg"]:
            image_ext = "jpeg"
        dest_image_path = f"{dest_image_base}.{image_ext}"
        shutil.copy2(imagePath, dest_image_path)
        imagePath = dest_image_path
    else:
        imagePath = "assets/icon2.png"

    new_song = {
        "name": songName,
        "src": songPath,
        "img": imagePath,
        "volume": 50,
        "shortcut": ""
    }

    try:
        with open("data/sounds.json", "r") as file:
            sounds = json.load(file)
    except FileNotFoundError:
        sounds = []

    sounds.append(new_song)

    with open("data/sounds.json", "w") as file:
        json.dump(sounds, file, indent=4)

def modify_settings_song(name, volume, shortcut):
    with open("data/sounds.json", "r") as f:
        sounds = json.load(f)

    for sound in sounds:
        if sound["name"] == name:
            sound["volume"] = volume
            sound["shortcut"] = shortcut
            break
    else:
        print(f"❌ Aucun son trouvé avec le nom : {name}")
        return

    with open("data/sounds.json", "w") as f:
        json.dump(sounds, f, indent=4)

    print("✅ Données mises à jour")
