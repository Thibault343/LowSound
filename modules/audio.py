import sounddevice as sd
import soundfile as sf
import time

last_time_played = 0
cooldown = 4
# ------------------------------------------------
# Function: play_sound
# Arguments:
#   - sound (str): The file path of the sound to be played.
#   - selected_device (str): The name of the audio output device.
#   - volume (int or float): The playback volume percentage (0-100).
# Description:
#   Plays the specified sound file on the selected audio device at the given volume.
#   - Converts volume percentage to a 0.0-1.0 scale.
#   - Finds the audio device matching the selected device name.
#   - Reads the sound file data and sample rate.
#   - Plays the sound scaled by the volume on the chosen device.
#   - Catches and prints errors if playback fails or if the device is not found.
# ------------------------------------------------
def play_sound(sound, selected_device, volume):
    global last_time_played
    time_know = time.time() #Get the actual time
    stop_play()
    if (time_know - last_time_played) > cooldown:
        try:
            print(f"| Sound Played |")
            last_time_played = time_know
            volume = volume / 100.0
            device_info = next((d for d in sd.query_devices() if d['name'] == selected_device), None)
            if device_info:
                try:
                    data, samplerate = sf.read(sound)
                    sd.play(data * volume, samplerate=samplerate, device=device_info['name'])
                except Exception as e:
                    print(f"Error playing sound: {e}")
            else:
                print("Selected device not found.")
        except:
            print("Sound can't be played")

# ------------------------------------------------
# Function: stop_play
# Arguments: None
# Description:
#   Stops any ongoing sound playback.
#   Catches and prints errors if stopping playback fails.
# ------------------------------------------------
def stop_play():
    try:
        sd.stop()
        print("Playback paused.")
    except Exception as e:
        print(f"Error pausing playback: {e}")
