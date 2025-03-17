import asyncio
import random
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN, WEATHER_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def get_weather(city: str) -> str:
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "ru"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(base_url, params=params) as response:
            if response.status != 200:
                return "Город не найден ❌"

            data = await response.json()
            weather = data["weather"][0]["description"].capitalize()
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]

            return (
                f"🌤 Погода в {city}:\n"
                f"➖ Состояние: {weather}\n"
                f"🌡 Температура: {temp}°C\n"
                f"💧 Влажность: {humidity}%\n"
                f"🌪 Ветер: {wind} м/с"
            )


# Команда для получения погоды
@dp.message(Command("weather"))
async def weather_command(message: Message):
    try:
        city = message.text.split(maxsplit=1)[1]
        weather = await get_weather(city)
        await message.answer(weather)
    except IndexError:
        await message.answer("Укажите город после команды /weather")


@dp.message(Command('photo'))
async def photo(message: Message):
    image_links = [
        'https://i.pinimg.com/236x/c8/cc/24/c8cc24bba37a25c009647b8875aae0e3.jpg',
        'https://img.freepik.com/free-photo/nature-animals_1122-1999.jpg',
        'https://img.freepik.com/free-photo/cute-cat-spending-time-indoors_23-2150649172.jpg'
    ]
    rand_photo = random.choice(image_links)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')


@dp.message(F.photo)
async def react_photo(message: Message):
    responses = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(responses)
    await message.answer(rand_answ)


@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer(
        'Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ'
    )


@dp.message(Command('help'))
async def help_command(message: Message):
    help_text = (
        "🤖 Доступные команды:\n"
        "/start - Начало работы\n"
        "/help - Помощь\n"
        "/photo - Получить случайное фото\n"
        "/weather [город] - Узнать погоду"
    )
    await message.answer(help_text)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Приветики, я бот! ✨")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())