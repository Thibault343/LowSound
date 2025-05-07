# LowSound

## What is it ?

LowSound is a simple soundboard you can use to play some sound in ur microphone.

## What can we use ?

For create this app we use Python for main programming language.

Some libraries :

-   sounddevice
-   soudfile

One external app:

-   Virtual Audio Cable app

## Run the app

### Requirements

-   [Python](https://www.python.org/downloads/) version : 3.13
-   [Flet](https://flet.dev/) version : 0.27.6
-   [Sounddevice](https://pypi.org/project/sounddevice/) version : 0.5.1
-   [Soundfile](https://pypi.org/project/soundfile/) versions : 0.13.1
-   [VB CABLE](https://vb-audio.com/Cable/)

### Installing packages

```python
pip install "flet==0.27.6" "sounddevice==0.5.1" "soundfile==0.13.1"
```

### Install VB CABLE

Go to [Download](https://vb-audio.com/Cable/)

### Setup VB Cable

1. Open your sounds settings
2. Go to Playback and select you headphone as default
3. Go to Recording and select your microphone as default
4. Go to Recording -> your microphone -> proprieties -> Listen to this device ✅
5. Select the output audio cable as a playback

### Start the app.js

```bash
./app.js
```

## Licenses

This project is licensed under the [MIT License](LICENSE).
