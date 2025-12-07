import pyaudio
import vosk
import json
import requests
import numpy as np   # added for FFT processing

#Flask Server
SERVER_URL = "http://172.20.10.4:6767/add_entry"

#load speech model for speech to text
model = vosk.Model("/home/pi/Documents/github/EE250/Final_Project/vosk-model-small-en-us-0.15")
recognizer = vosk.KaldiRecognizer(model, 16000)

#set microphone settings
RATE = 16000
CHUNK = 4000


# Send text and frequency to Flask server after conversion
def send_to_server(text, frequency, freqs, mags):

    payload = {
        "text": text,
        "frequency": frequency,          # dominant frequency (Hz)
        "frequencies": freqs,            # full frequency axis
        "magnitudes": mags               # full spectrum magnitudes
    }

    try:
        response = requests.post(SERVER_URL, json=payload)

        if response.status_code == 200:
            print("Sent to server:", payload["text"], f"(dominant={frequency} Hz)")
        else:
            print("Server error:", response.text)

    except requests.exceptions.RequestException as e:
        print("Failed to send data:", e)


# --- FFT PROCESSING FUNCTION ---
def compute_fft(data):
    """
    Compute FFT spectrum from the raw microphone audio chunk.
    Returns: (dominant_frequency, frequency_axis_list, magnitude_list)
    """

    # Convert PCM bytes to numpy int16
    samples = np.frombuffer(data, dtype=np.int16).astype(float)

    # Remove DC offset
    samples = samples - np.mean(samples)

    # Apply Hann window
    window = np.hanning(len(samples))
    samples = samples * window

    # FFT
    fft_result = np.fft.rfft(samples)

    # Magnitude spectrum
    magnitudes = np.abs(fft_result)

    # Frequency axis
    freqs = np.fft.rfftfreq(len(samples), 1.0 / RATE)

    # Dominant frequency
    idx = np.argmax(magnitudes)
    dominant_freq = float(freqs[idx])

    return dominant_freq, freqs.tolist(), magnitudes.tolist()



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

                    # ---- FFT PROCESSING HERE ----
                    dom_freq, freqs, mags = compute_fft(data)

                    # Send the data to your Flask server
                    send_to_server(detected_text, dom_freq, freqs, mags)

    except KeyboardInterrupt:
        print("\nMicrophone stopped")

    # stop microphone
    stream.stop_stream()
    stream.close()
    audio.terminate()


if __name__ == "__main__":
    main()

