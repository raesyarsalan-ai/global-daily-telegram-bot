from aiogram.types import Message
from services.weather import WeatherService


async def weather_handler(message: Message):
    """
    Usage:
    /weather London
    """
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.answer("🌍 Please enter a city name.\nExample:\n/weather Berlin")
        return

    city = args[1]
    weather_text = WeatherService.get_current_weather(city)

    await message.answer(weather_text)
