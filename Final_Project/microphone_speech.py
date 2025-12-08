import pyaudio
import vosk
import json
import requests
import numpy as np

#Flask Server
SERVER_URL = "http://172.20.10.4:6767/add_entry"

#load speech model for speech to text
model = vosk.Model("/home/pi/Documents/github/EE250/Final_Project/vosk-model-small-en-us-0.15")
recognizer = vosk.KaldiRecognizer(model, 16000)


# Send text and frequency to Flask server after conversion
def send_to_server(text, freqs, mags):

    payload = {"text": text, "frequencies": freqs, "magnitudes": mags}

    response = requests.post(SERVER_URL, json=payload)

    if response.status_code == 200:
        print("Text sent to server")
    else:
        print("Error:", response.text)


# function for FFT
def compute_fft(data):

    #convert data into ints (from bytes)
    samples = np.frombuffer(data, dtype=np.int16).astype(float)

    # remove any DC offset
    samples = samples - np.mean(samples)

    #Hann window
    window = np.hanning(len(samples))
    samples = samples * window

    #FFT
    fft_result = np.fft.rfft(samples)

    #get relative magnitudes
    mags = np.abs(fft_result)

    #store actual frequencies
    freqs = np.fft.rfftfreq(len(samples), 1.0 / 16000) #(16000 is rate)

    #return the frequencies and magnitudes as lists
    return list(freqs), list(mags)



def main():
    #Start microphone (used ChatGPT to help set up microphone recording)
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)

    print("Microphone Started")

    try:
        while True:
            #used ChatGPT to help with Vosk library syntax
            # Read small audio portion
            data = stream.read(4000, exception_on_overflow=False)

            #after full phrase is detected:
            if recognizer.AcceptWaveform(data):
                #get the result from the json file as a dict
                result = json.loads(recognizer.Result())
                #extract the text from the dict
                text = result.get("text", "").strip()

                print(text)

                # call FFT function to process data
                freqs, mags = compute_fft(data)

                #filter out frequencies below 65 Hz
                filtered = [(f, m) for f, m in zip(freqs, mags) if f > 65]
                #get them back into separate lists (unzip them)
                freqs, mags = zip(*filtered)
                freqs = list(freqs)
                mags = list(mags)

                # Send all data to Flask server
                send_to_server(text, freqs, mags)

    #ensure microphone is stopped correctly to avoid future issues
    # (used ChatGPT to help)
    except KeyboardInterrupt:
        print("Microphone stopped")

    # stop microphone
    stream.stop_stream()
    stream.close()
    audio.terminate()


if __name__ == "__main__":
    main()