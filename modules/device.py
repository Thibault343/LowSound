import sounddevice as sd

# ------------------------------------------------
# Function: get_output_devices
# Arguments: None
# Description:
#   Retrieves a list of available audio output devices.
#   Filters out devices that do not support audio output (i.e., max_output_channels <= 0).
# Returns:
#   List of device names (strings) that can output audio.
# ------------------------------------------------
def get_output_devices():
    devices = sd.query_devices()
    return [d['name'] for d in devices if d['max_output_channels'] > 0]
