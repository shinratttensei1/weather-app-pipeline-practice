import requests
import os
from dotenv import load_dotenv
from dataclasses import dataclass
from requests.exceptions import Timeout
load_dotenv()


API_key=os.getenv('API_KEY')

@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: int
    feels_like: int

def get_weather(city_name, API_key):
    try:
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}&units=metric',
            timeout=10  
        )
        response.raise_for_status()  

        response_json = response.json()

        if 'weather' not in response_json or 'main' not in response_json:
            raise ValueError("Invalid API response. Missing required fields.")

        weather = response_json['weather'][0]
        main_data = response_json['main']

        data = WeatherData(
            main=weather.get('main'),
            description=weather.get('description'),
            icon=weather.get('icon'),
            temperature=round(main_data.get('temp')),
            feels_like=round(main_data.get('feels_like'))
        )

        return data
    
    except Timeout:
        raise ValueError("Timeout occurred while trying to fetch weather data")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"An error occured while fetching weather data. {e}")


def main(city_name):
    weather_data = get_weather(city_name, API_key)
    return weather_data

if __name__ == '__main__':
    print(get_weather('Astana', API_key))
