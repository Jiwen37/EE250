import requests

SERVER_URL = "http://10.23.38.236:6767/add"   

def main():
    print("Type 'exit' at any time to quit.")

    while True:
        text = input("Enter text: ")
        if text.lower() == "exit":
            break

        freq = input("Enter frequency (Hz): ")
        if freq.lower() == "exit":
            break

        # Validate frequency
        try:
            freq = float(freq)
        except ValueError:
            print("Invalid frequency. Must be a number.\n")
            continue

        payload = {
            "text": text,
            "frequency": freq
        }

        try:
            response = requests.post(SERVER_URL, json=payload)
            if response.status_code == 200:
                print("Data sent successfully.\n")
            else:
                print("Server error:", response.text, "\n")

        except requests.exceptions.RequestException as e:
            print("Failed to send data:", e, "\n")

if __name__ == "__main__":
    main()
