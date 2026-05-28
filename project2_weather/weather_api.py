"""
Project 2: Weather API Data Extraction
Uses Open-Meteo API (FREE, no key needed!)
Fetches current weather + 7-day forecast for any city
"""

import requests
import json
from datetime import datetime


# Step 1: Get coordinates from city name using Open-Meteo Geocoding API
def get_coordinates(city_name):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name, "count": 1, "language": "en", "format": "json"}

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if not data.get("results"):
        raise ValueError(f"City '{city_name}' not found.")

    result = data["results"][0]
    return {
        "city": result["name"],
        "country": result.get("country", ""),
        "lat": result["latitude"],
        "lon": result["longitude"],
    }


# Step 2: Fetch weather data
def get_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
        "timezone": "auto",
        "forecast_days": 7,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def weather_code_to_description(code):
    codes = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Foggy", 48: "Icy fog", 51: "Light drizzle", 61: "Slight rain",
        63: "Moderate rain", 65: "Heavy rain", 71: "Slight snow", 80: "Rain showers",
        95: "Thunderstorm",
    }
    return codes.get(code, f"Code {code}")


def display_weather(city_info, weather_data):
    current = weather_data["current"]
    daily = weather_data["daily"]

    print(f"\n{'='*50}")
    print(f"  Weather for {city_info['city']}, {city_info['country']}")
    print(f"{'='*50}")
    print(f"  Condition  : {weather_code_to_description(current['weather_code'])}")
    print(f"  Temperature: {current['temperature_2m']}°C")
    print(f"  Humidity   : {current['relative_humidity_2m']}%")
    print(f"  Wind Speed : {current['wind_speed_10m']} km/h")
    print(f"\n  7-Day Forecast:")
    print(f"  {'Date':<14} {'Max':>6} {'Min':>6} {'Rain':>8}  Condition")
    print(f"  {'-'*55}")

    for i in range(7):
        date = daily["time"][i]
        max_t = daily["temperature_2m_max"][i]
        min_t = daily["temperature_2m_min"][i]
        rain = daily["precipitation_sum"][i]
        desc = weather_code_to_description(daily["weather_code"][i])
        print(f"  {date:<14} {max_t:>5}°C {min_t:>5}°C {rain:>6}mm  {desc}")

    print()


def save_weather_json(city_info, weather_data, f"project2_weather/weather_{city.lower().replace(' ', '_')}.json"):
    output = {"city": city_info, "fetched_at": datetime.now().isoformat(), "data": weather_data}
    with open(filename, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Data saved to {filename}")


if __name__ == "__main__":
    cities = ["Delhi", "London", "New York"]

    for city in cities:
        try:
            city_info = get_coordinates(city)
            weather_data = get_weather(city_info["lat"], city_info["lon"])
            display_weather(city_info, weather_data)
            save_weather_json(city_info, weather_data, f"weather_{city.lower().replace(' ', '_')}.json")
        except Exception as e:
            print(f"Error fetching weather for {city}: {e}")

