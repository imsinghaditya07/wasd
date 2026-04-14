# SilentBridge

SilentBridge is a bi-directional communication system designed for deaf/mute individuals to converse with hearing individuals. It operates entirely offline (except for standard STT on Google's free tier).

## Features
- **Sign → Speech (Mode 1)**: Uses a webcam to detect hand gestures, translates them into text, and reads them out loud.
- **Speech → Sign (Mode 2)**: Listens to spoken words, converts them to text, and maps them to animated ASL signs.

## Requirements
- Python 3.8+
- Webcam
- Microphone

Libraries (see `requirements.txt`):
- `opencv-python`
- `mediapipe`
- `scikit-learn`
- `numpy`
- `pyttsx3`
- `SpeechRecognition`
- `PyAudio`
- `Pillow`
- `pandas`
- `joblib`

## Installation

```bash
# Clone the repository and navigate into it
cd silentbridge

# Install dependencies
pip install -r requirements.txt
```

### Note on PyAudio
- **Windows**: If `pip install pyaudio` fails, you may need to use `pipwin`: `pip install pipwin && pipwin install pyaudio`
- **Linux**: You will need system-level audio headers: `sudo apt-get install portaudio19-dev python3-pyaudio`
- **Mac**: Use Homebrew: `brew install portaudio` before `pip install pyaudio`

## Usage

Before running the application for the first time, you must train the gesture recognition model.

### 1. Collect Training Data
```bash
python training/collect_data.py
```
Type a label (e.g. "hello"), then hold your hand to the camera and press 'c' to collect 100 samples. Do this for all desired words.

### 2. Train the Model
```bash
python training/train_model.py
```
This will process the collected data and output `models/gesture_classifier.pkl`.

### 3. Run the App
```bash
python main.py
```
Switch between the modes via the top navigation bar.

## How to Add New Signs
To add more signs for "Speech → Sign" mode:
1. Download a GIF of the sign.
2. Place it into `data/signs/`.
3. Update `data/sign_dictionary.json` with the new word to path mapping.

## Troubleshooting
- **Camera errors**: Ensure no other application (Zoom, Teams, etc.) is currently using your camera.
- **Microphone errors**: Check system audio settings to ensure your default recording device is enabled and functional.
