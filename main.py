import asyncio
import random
import aiohttp
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from gtts import gTTS
from googletrans import Translator
from config import TOKEN, WEATHER_API_KEY
import keyboards as kb


bot = Bot(token=TOKEN)
dp = Dispatcher()

os.makedirs("tmp", exist_ok=True)
os.makedirs("img", exist_ok=True)

translator = Translator()

@dp.message(F.text == "Привет")
async def hello_handler(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}! ✨")

@dp.message(F.text == "Пока")
async def bye_handler(message: Message):
    await message.answer(f"До свидания, {message.from_user.first_name}! 👋")

@dp.message(Command("links"))
async def links_command(message: Message):
    await message.answer("Ссылки на ресурсы:", reply_markup=kb.links)

@dp.message(Command("dynamic"))
async def dynamic_command(message: Message):
    await message.answer("Динамическое меню:", reply_markup=kb.dynamic_keyboard())

@dp.callback_query(F.data == "show_more")
async def show_more_handler(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=kb.dynamic_keyboard(show_more=True))
    await callback.answer()

@dp.callback_query(F.data.startswith("option_"))
async def option_handler(callback: types.CallbackQuery):
    option = callback.data.split("_")[1]
    await callback.message.answer(f"Выбрана опция {option} ✅")
    await callback.answer()

@dp.message(Command('video'))
async def video(message: Message):
    try:
        await bot.send_chat_action(message.chat.id, 'upload_video')
        video = FSInputFile('video.mp4')
        await bot.send_video(message.chat.id, video)
    except FileNotFoundError:
        await message.answer("Видеофайл не найден.")
    except Exception as e:
        await message.answer(f"Ошибка при отправке видео: {str(e)}")

@dp.message(Command('voice'))
async def voice(message: Message):
    try:
        voice_file = FSInputFile("sample.ogg")
        await bot.send_voice(message.chat.id, voice_file)
    except FileNotFoundError:
        await message.answer("Голосовой файл не найден.")
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")

@dp.message(Command('audio'))
async def audio(message: Message):
    try:
        audio_file = FSInputFile('sound2.mp3')
        await bot.send_audio(message.chat.id, audio_file)
    except FileNotFoundError:
        await message.answer("Аудиофайл не найден.")
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")

@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
        "Тренировка 1:\n1. Скручивания: 3x15\n2. Велосипед: 3x20\n3. Планка: 3x30 сек",
        "Тренировка 2:\n1. Подъемы ног: 3x15\n2. Русский твист: 3x20\n3. Планка с ногой: 3x20 сек",
        "Тренировка 3:\n1. Скручивания с ногами: 3x15\n2. Ножницы: 3x20\n3. Боковая планка: 3x20 сек"
    ]

    rand_tr = random.choice(training_list)
    await message.answer(f"🏋️ Ваша мини-тренировка на сегодня:\n\n{rand_tr}")

    try:
        tts = gTTS(text=rand_tr, lang='ru')
        filename = "tmp/training.ogg"
        tts.save(filename)
        await bot.send_voice(chat_id=message.chat.id, voice=FSInputFile(filename))
        os.remove(filename)
    except Exception as e:
        await message.answer(f"Ошибка при озвучивании тренировки: {str(e)}")

@dp.message(Command('help'))
async def help_command(message: Message):
    help_text = (
        "🤖 Доступные команды:\n"
        "/start - Начало работы\n"
        "/help - Помощь\n"
        "/photo - Получить случайное фото\n"
        "/weather [город] - Узнать погоду\n"
        "/training - Получить тренировку с озвучкой\n"
        "/voice - Получить голосовое сообщение\n"
        "/doc - Получить документ\n"
        "/video - Получить видео\n"
        "/audio - Получить аудиофайл\n"
        "/links - Полезные ссылки\n"
        "/dynamic - Динамическое меню\n"
    )
    await message.answer(help_text)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}! ✨', reply_markup=kb.main)

async def main():
    await dp.start_polling(bot)

@dp.message(Command('doc'))
async def doc(message: Message):
    try:
        document = FSInputFile("Krug.pdf")
        await bot.send_document(message.chat.id, document)
    except FileNotFoundError:
        await message.answer("Документ не найден.")
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")

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
                f"➖ {weather}\n"
                f"🌡 {temp}°C\n"
                f"💧 {humidity}%\n"
                f"🌪 {wind} м/с"
            )

@dp.message(Command("weather"))
async def weather_command(message: Message):
    try:
        city = message.text.split(maxsplit=1)[1]
        weather = await get_weather(city)
        await message.answer(weather)
    except IndexError:
        await message.answer("Укажите город после команды /weather.")
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")

@dp.message(Command('photo'))
async def photo(message: Message):
    image_links = [
        'https://i.pinimg.com/236x/c8/cc/24/c8cc24bba37a25c009647b8875aae0e3.jpg',
        'https://img.freepik.com/free-photo/nature-animals_1122-1999.jpg',
        'https://img.freepik.com/free-photo/cute-cat-spending-time-indoors_23-2150649172.jpg'
    ]
    await message.answer_photo(photo=random.choice(image_links), caption='Вот ваша картинка!')

@dp.message(F.text)
async def translate_text(message: Message):
    try:
        translated = await translator.translate(message.text, dest='en')
        await message.answer(f"Переведённый текст: {translated.text}")
    except Exception as e:
        await message.answer(f"Ошибка при переводе текста: {str(e)}")



if __name__ == "__main__":
    asyncio.run(main())
