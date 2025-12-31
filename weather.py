import requests
from config import WEATHER_API_KEY

def weather_by_coords(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
    r = requests.get(url).json()
    return f"{r['weather'][0]['description']} | {r['main']['temp']}°C"
