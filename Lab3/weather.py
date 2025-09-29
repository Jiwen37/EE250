import requests
import json
import pprint

# WeatherAPI key
WEATHER_API_KEY = ''  # TODO: Replace with your own WeatherAPI key

def get_weather(city):
    # TODO: Build the API request URL using the base API endpoint, the API key, and the city name provided by the user.
    URL = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
    
    # TODO: Make the HTTP request to fetch weather data using the 'requests' library.
    response = requests.get(URL)
    
    # TODO: Handle HTTP status codes:
    # - Check if the status code is 200 (OK), meaning the request was successful.
    # - If not 200, handle common errors like 400 (Bad Request), 401 (Unauthorized), 404 (Not Found), and any other relevant codes.
    # NOTE TO SELF-> FIGURE OUT HOW TO HANDLE
    if response.status_code == 200:
        print("200:success")
        # TODO: Parse the JSON data returned by the API. Extract and process the following information:
        data = response.json()
        # - Current temperature in Fahrenheit
        tempf = data['current']['temp_f']
        # - The "feels like" temperature
        feels_like = data['current']['feelslike_f']
        # - Weather condition (e.g., sunny, cloudy, rainy)
        w_condition = data['current']['condition']['text']
        # - Humidity percentage
        humidity = data['current']['humidity']
        # - Wind speed and direction
        wind_mph = data['current']['wind_mph']
        wind_dir = data['current']['wind_dir']
        # - Atmospheric pressure in mb
        atm_pres = data['current']['pressure_mb']
        # - UV Index value
        uv = data['current']['uv']
        # - Cloud cover percentage
        cloud_cover = data['current']['cloud']
        # - Visibility in miles
        vis_miles = data['current']['vis_miles']
        print(f"Weather data for {city}...\n")
        print(f"Temperature in Fahrenheit: {tempf}F\n")
        print(f"Feels like: {feels_like}F\n")
        print(f"Weather condition: {w_condition}\n")
        print(f"Humidity: {humidity}%\n")
        print(f"Weather condition: {w_condition}\n")
        print(f"Wind speed and direction: {wind_mph} mph {wind_dir}\n")
        print(f"Atmospheric Pressure: {atm_pres} mb\n")
        print(f"UV index value: {uv}\n")
        print(f"Cloud cover percentage: {cloud_cover}\n")
        print(f"Visibility: {vis_miles} miles\n")
        #pprint.pprint(data)

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
    # TODO: Prompt the user to input a city name.
    city = input("Choose a city\n")
    
    # TODO: Call the 'get_weather' function with the city name provided by the user.
    get_weather(city)
    pass
