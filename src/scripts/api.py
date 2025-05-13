import sounddevice as sd
import soundfile as sf
import shutil
import json
import os

# Get a list of all available output audio devices
def get_output_devices():
    """
    Returns a list of available output audio device names.
    """
    devices = sd.query_devices() 
    output_devices = [d['name'] for d in devices if d['max_output_channels'] > 0]
    return output_devices

# List all available sound files listed in the JSON storage
def list_sounds(name, onefile):
    """
    Returns a list of .wav files from the sound folder.
    """
    try:
        with open("storage/data/sounds.json", "r") as f:
            sounds = json.load(f)
            return sounds
    except FileNotFoundError:
        print("Sounds file not found. Using default sounds.")
        return ["sound1.mp3", "sound2.mp3"]
    
# Save selected device and theme to settings.json
def saved_settings(dropdown_device, dropdown_theme):
    with open('storage/data/settings.json', 'r+') as f:
        settings = json.load(f)
        if settings['device'] != dropdown_device.value:
            settings['device'] = dropdown_theme.value
        if settings['default_theme'] != dropdown_theme.value:
            settings['default_theme'] = dropdown_theme.value
        f.seek(0)
        json.dump(settings, f, indent=4)
        f.truncate()

# Delete a song from JSON and filesystem
def delete_song_from_json(e):
    with open("storage/data/sounds.json", 'r') as f:
        data = json.load(f)

    # Remove the song with the matching name
    data = [song for song in data if song['name'] != e['name']]

    # Write updated data back to JSON file
    with open("storage/data/sounds.json", 'w') as f:
        json.dump(data, f, indent=4)

    # Remove the sound file from storage
    os.remove(e["src"])
    os.remove(e["img"])

# Play a sound on the selected output device
def play_sound(sound, selected_device):
    device_name = selected_device  # Already a string
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

# Pause or resume sound playback
def pause_and_play():
    """
    Pauses or resumes playback depending on the current state.
    """
    try:
        sd.stop()
        print("Playback paused.")
    except Exception as e:
        print(f"Error pausing playback: {e}")

# Stop sound playback
def stop_sound():
    try:
        sd.stop()
        print("Playback stopped.")
    except Exception as e:
        print(f"Error stopping sound: {e}")

# Entry point to list all output devices
def main():
    print("🔊 Searching for audio output devices...")
    output_devices = get_output_devices()
    
    if not output_devices:
        print("❌ No output audio devices found.")
    else:
        print("✅ Devices detected:")
    
    return output_devices

# Create and save a new song entry (copy audio/image files, update JSON)


def createNewSong(songName, songPath, imagePath):
    # Use default image if none selected
    if imagePath == "Aucune image sélectionné":
        imagePath = "../assets/icon2.png"

    # Proceed only if the song name is not empty or just spaces
    if songName.strip() != "":
        # Get the song file extension
        songType = songPath.split(".")[-1].lower()
        # Destination paths
        default_song_path = "storage/data/sounds/"
        dest_song_path = f"{default_song_path}{songName}.{songType}"
        dest_image_base = f"storage/data/images/{songName}"

        # Check if source files exist
        src_song_file_exists = os.path.isfile(songPath)
        src_image_file_exists = os.path.isfile(imagePath)
        # Verify if the song existing
        dest_song_exists = os.path.isfile(dest_song_path)
        # If the song already exists, append an index to the name
        if dest_song_exists:
            i = 0
            # Increment the index until a unique name is found
            while dest_song_exists:
                i += 1
                dest_song_exists = os.path.isfile(f"{default_song_path}{songName}({i}).{songType}")
            dest_song_path = f"{default_song_path}{songName}({i}).{songType}"
            dest_image_base = f"storage/data/images/{songName}({i})"
            songName = f"{songName}({i})"

            
        # Copy song if valid
        if src_song_file_exists:
            shutil.copy2(songPath, dest_song_path)
            songPath = dest_song_path  # Update to new location

        # Copy image if valid and set appropriate extension
        if src_image_file_exists:
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
        new_song = {
            "name": songName,
            "src": songPath if os.path.isfile(songPath) else "",
            "img": imagePath if os.path.isfile(imagePath) else "../assets/icon2.png"
        }

        # Read existing songs and append the new one
        try:
            with open("storage/data/sounds.json", "r") as file:
                sounds = json.load(file)
        except FileNotFoundError:
            sounds = []  # Start with empty list if file does not exist

        sounds.append(new_song)

        # Write updated list back to the file
        with open("storage/data/sounds.json", "w") as file:
            json.dump(sounds, file, indent=4)
        
            


    

                


# Run the main function if script is executed directly
if __name__ == "__main__":

    main()
