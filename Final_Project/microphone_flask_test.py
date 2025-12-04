import pyaudio
import vosk
import json
import requests

# Only load keyboard control if enabled
ENABLE_KEY_CONTROL = True
if ENABLE_KEY_CONTROL:
    import keyboard   # listens for "a" and "s" keys


# ---------------------------
# Server information
# ---------------------------
SERVER_URL = "http://10.23.38.236:6767/add"


# ---------------------------
# Load the Vosk STT model
# ---------------------------
model = vosk.Model("/home/pi/Documents/github/EE250/Final_Project/vosk-model-small-en-us-0.15")
recognizer = vosk.KaldiRecognizer(model, 16000)

# Microphone audio settings
RATE = 16000
CHUNK = 1024


# ---------------------------
# Function: send text + frequency to server
# ---------------------------
def send_to_server(text, frequency):
    """Send recognized text to Flask server (your original client code)."""

    payload = {
        "text": text,
        "frequency": frequency
    }

    try:
        response = requests.post(SERVER_URL, json=payload)

        if response.status_code == 200:
            print("✓ Sent to server:", payload)
        else:
            print("Server error:", response.text)

    except requests.exceptions.RequestException as e:
        print("Failed to send data:", e)


# ---------------------------
# Optional: Keyboard-based start/stop logic
# ---------------------------
listening = True  # starts ON by default; keyboard can change it


def update_listening_state():
    """Update microphone on/off based on key presses."""
    global listening

    if not ENABLE_KEY_CONTROL:
        return  # If key control disabled, ignore

    # "a" key starts listening
    if keyboard.is_pressed("a") and not listening:
        listening = True
        print("Microphone ON")

    # "s" key stops listening
    if keyboard.is_pressed("s") and listening:
        listening = False
        print("Microphone OFF")


# ---------------------------
# Main microphone + Vosk loop
# ---------------------------
def main():
    global listening

    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    # Display key instructions only if enabled
    if ENABLE_KEY_CONTROL:
        print("Press 'a' to START, 's' to STOP.")
    else:
        print("Listening... (Ctrl+C to stop)")

    try:
        while True:
            # Check keyboard keys (if enabled)
            update_listening_state()

            # Only process audio if microphone is ON
            if listening:
                data = stream.read(CHUNK, exception_on_overflow=False)

                # Check for full phrase
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "").strip()

                    if text:
                        print("You said:", text)

                        # Placeholder for now
                        freq = 0.0

                        # Send to your server
                        send_to_server(text, freq)

    except KeyboardInterrupt:
        print("\nStopping program...")

    stream.stop_stream()
    stream.close()
    audio.terminate()


if __name__ == "__main__":
    main()
