import requests
from config import WEATHER_API_KEY


class WeatherService:
    BASE_URL = "https://api.weatherapi.com/v1"

    @staticmethod
    def get_current_weather(city: str, lang: str = "en") -> str:
        """
        Get current weather by city name
        """
        url = f"{WeatherService.BASE_URL}/current.json"
        params = {
            "key": WEATHER_API_KEY,
            "q": city,
            "lang": lang,
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if "error" in data:
                return "❌ Weather data not available."

            condition = data["current"]["condition"]["text"]
            temp_c = data["current"]["temp_c"]
            humidity = data["current"]["humidity"]
            wind_kph = data["current"]["wind_kph"]

            return (
                f"🌤 Weather in {city}\n"
                f"Condition: {condition}\n"
                f"🌡 Temperature: {temp_c}°C\n"
                f"💧 Humidity: {humidity}%\n"
                f"💨 Wind: {wind_kph} km/h"
            )

        except Exception:
            return "⚠️ Weather service unavailable."
