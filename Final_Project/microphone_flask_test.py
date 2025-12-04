import pyaudio
import vosk
import json
import requests

# ---------------------------
# Server information (from your client code)
# ---------------------------
SERVER_URL = "http://10.23.38.236:6767/add"

# ---------------------------
# Load the Vosk speech model
# ---------------------------
model = vosk.Model("/home/pi/Documents/github/EE250/Final_Project/vosk-model-small-en-us-0.15")
recognizer = vosk.KaldiRecognizer(model, 16000)

# Microphone audio settings
RATE = 16000
CHUNK = 1024


def send_to_server(text, frequency):
    """
    Send the text and frequency to your Flask server.
    This function uses your original client code logic.
    """

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


def main():
    # Start the microphone
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("Listening... (Ctrl+C to stop)")

    try:
        while True:
            # Read a small piece of audio
            data = stream.read(CHUNK, exception_on_overflow=False)

            # When Vosk detects a full spoken phrase
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip()

                # If we recognized real speech
                if text:
                    print("You said:", text)

                    # Use recognized speech as the "text" field
                    detected_text = text

                    # Placeholder frequency for now
                    detected_frequency = 0.0

                    # Send the data to your Flask server
                    send_to_server(detected_text, detected_frequency)

    except KeyboardInterrupt:
        print("\nStopping...")

    # Close the microphone when done
    stream.stop_stream()
    stream.close()
    audio.terminate()


if __name__ == "__main__":
    main()
