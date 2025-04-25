from customtkinter import *
import sounddevice as sd
import soundfile as sf
from os import listdir

app = CTk()
app.geometry("400x240")
app.title("CustomTkinter Example")

# Function to play sound on the selected output device
def play_sound(sound):
    global selected_device
    device_name = selected_device.get()
    device_info = next((d for d in devices if d['name'] == device_name), None)
    if device_info:
        try:
            file_path = f"./sounds/{sound}.mp3"
            data, samplerate = sf.read(file_path)
            sd.play(data, samplerate=samplerate, device=device_info['name'])
        except Exception as e:
            print(f"Error playing sound: {e}")
    else:
        print("Selected device not found.")

# Function to refresh the sound list
def get_sound_list():
    global scrollable_frame
    try:
        scrollable_frame.pack_forget()
    except:
        print("No scrollable frame to destroy.")
    scrollable_frame = CTkScrollableFrame(app, width=380, height=150)
    scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)
    sound_list = []
    files = listdir('./sounds')
    for sound in files:
        if sound.endswith('.mp3'):
            sound_list.append(sound[:-4])
    
    for sound in sound_list:
        sound_button = CTkButton(scrollable_frame, text=sound, command=lambda s=sound: play_sound(s), width=350)
        sound_button.pack(pady=5)
    return sound_list

# Get available audio devices
devices = sd.query_devices()
output_devices = [d['name'] for d in devices if d['max_output_channels'] > 0]

# Handle case where no output devices are found
if output_devices:
    selected_device = StringVar(value=output_devices[0])
else:
    print("No valid output devices found.")
    selected_device = StringVar(value="No Device")

# Dropdown menu for selecting output device
device_menu = CTkOptionMenu(app, values=output_devices, variable=selected_device)
device_menu.pack(pady=10)

refresh_button = CTkButton(app, text="Refresh", command=lambda: get_sound_list()).pack()

sound_list = get_sound_list()
print(sound_list)

app.mainloop()