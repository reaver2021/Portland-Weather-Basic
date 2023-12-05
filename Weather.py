import os
import requests
from dotenv import load_dotenv

load_dotenv("config.env")

def get_weather(api_key, latitude, longitude):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": api_key,
        "units": "imperial"  # You can change units to metric, if preferred
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200: 
        weather_data = response.json()
        return weather_data
    else:
        return None

# Function to post weather information to Discord
def post_to_discord(webhook_url, message):
    payload = {
        "content": message
    }
    response = requests.post(webhook_url, json=payload)

    if response.status_code == 204:
        print("Message sent successfully to Discord!")
    else:
        print("Failed to send message to Discord.")
#To adjust where the messege is sent on discord, make sure to change the webhook within the config.env file.

api_key = os.getenv("api_key")
portland_latitude = os.getenv("portland_latitude")
portland_longitude = os.getenv("portland_longitude")
webhook_url = os.getenv("discord_webhook_url")

weather_info = get_weather(api_key, portland_latitude, portland_longitude)

if weather_info:
    temperature = weather_info['main']['temp']
    weather_description = weather_info['weather'][0]['description']
    message = f"The current temperature in Portland, Oregon is {temperature}°F with {weather_description}."

    post_to_discord(webhook_url, message)
else:
    print("Failed to fetch weather data.")