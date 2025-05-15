import sounddevice as sd
import soundfile as sf

def play_sound(sound, selected_device, volume):
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

def stop_play():
    try:
        sd.stop()
        print("Playback paused.")
    except Exception as e:
        print(f"Error pausing playback: {e}")
