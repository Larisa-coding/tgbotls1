import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from config import TOKEN, THE_CAT_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


def get_cat_breeds():
    url = "https://api.thecatapi.com/v1/breeds"
    headers = {"x-api-key": THE_CAT_API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching cat breeds: {e}")
        return []


def get_cat_image_by_breed(breed_id):
    url = f"https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}"
    headers = {"x-api-key": THE_CAT_API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data[0]['url'] if data else None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching cat image: {e}")
        return None


def get_breed_info(breed_name):
    breeds = get_cat_breeds()
    for breed in breeds:
        if breed['name'].lower() == breed_name.lower():
            return breed
    return None


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Hello! Send me a cat breed name, and I'll send you a photo and description.")


@dp.message()
async def send_cat_info(message: Message):
    breed_name = message.text.strip()
    breed_info = get_breed_info(breed_name)

    if breed_info:
        cat_image_url = get_cat_image_by_breed(breed_info['id'])
        if cat_image_url:
            info = (
                f"🐱 Breed: {breed_info['name']}\n"
                f"📖 Description: {breed_info['description']}\n"
                f"❤️ Life Span: {breed_info['life_span']} years"
            )
            await message.answer_photo(photo=cat_image_url, caption=info)
        else:
            await message.answer("Sorry, I couldn't find an image for this breed.")
    else:
        await message.answer("Breed not found. Please try again.")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
