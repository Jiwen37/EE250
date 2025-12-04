import pyaudio
import vosk
import json
import requests

#Flask Server
SERVER_URL = "http://10.23.38.236:6767/add"

#load speech model for speech to text
model = vosk.Model("/home/pi/Documents/github/EE250/Final_Project/vosk-model-small-en-us-0.15")
recognizer = vosk.KaldiRecognizer(model, 16000)

#set microphone settings
RATE = 16000
CHUNK = 1024


# Send text and frequency to Flask server after conversion
def send_to_server(text, frequency):

    payload = {
        "text": text,
        "frequency": frequency
    }

    try:
        response = requests.post(SERVER_URL, json=payload)

        if response.status_code == 200:
            print("Sent to server:", payload)
        else:
            print("Server error:", response.text)

    except requests.exceptions.RequestException as e:
        print("Failed to send data:", e)


def main():
    #Start microphone
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("Microphone Started")

    try:
        while True:
            # Read small audio portion
            data = stream.read(CHUNK, exception_on_overflow=False)

            #after full phrase is detected:
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip()

                # if text is generated from the sound (speech)
                if text:
                    print(text)

                    # Use recognized speech as the "text" field
                    detected_text = text

                    # Placeholder frequency for now
                    detected_frequency = 0.0

                    # Send the data to your Flask server
                    send_to_server(detected_text, detected_frequency)

    except KeyboardInterrupt:
        print("\nMicrophone stopped")

    # stop microphone
    stream.stop_stream()
    stream.close()
    audio.terminate()


if __name__ == "__main__":
    main()
