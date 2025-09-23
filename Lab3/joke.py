import requests
JOKE_API_KEY = ''
URL = f"https://official-joke-api.appspot.com/random_joke"

def get_joke():
    response = requests.get(URL)

    if response.status_code == 200:
        print("200:success")
        # TODO: Parse the JSON data returned by the API. Extract and process the following information:
        data = response.json()
        # - Current temperature in Fahrenheit
        setup = data['setup']
        punchline = data['punchline']
        print(f"{setup}")
        i = input('press anything to get answer\n')
        print(f"{punchline}")

    elif response.status_code == 400:
        print("400: bad request")
    elif response.status_code == 401:
        print("401: unauthorized")
    elif response.status_code == 404:
        print("404: not found")
        # TODO: Display the extracted weather information in a well-formatted manner.
    else:
        # TODO: Implement error handling for common status codes. Provide meaningful error messages based on the status code.
        print(f"Error: {response.status_code}. Something went wrong.")


if __name__ == '__main__':
    get_joke()
    pass