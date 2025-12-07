import pyaudio
import vosk
import json

# Load the Vosk STT model
model = vosk.Model("/home/pi/Documents/github/EE250/Final_Project/vosk-model-small-en-us-0.15")
recognizer = vosk.KaldiRecognizer(model, 16000)

# Microphone settings
RATE = 16000
CHUNK = 1024

def main():
    # Start microphone
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

            # Check if a full phrase was spoken
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip()

                # Print recognized speech
                if text:
                    print("You said:", text)

    except KeyboardInterrupt:
        print("\nStopping...")

    # Turn off microphone
    stream.stop_stream()
    stream.close()
    audio.terminate()

if __name__ == "__main__":
    main()
