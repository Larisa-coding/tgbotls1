import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from config import TOKEN, NEWS_API_KEY, EXCHANGE_RATE_API_KEY, WEATHER_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()

    if response.get("cod") != 200:
        return "❌ City not found!"

    temp = response["main"]["temp"]
    weather_desc = response["weather"][0]["description"]
    return f"🌤 **Weather in {city}:**\n🌡 Temperature: {temp}°C\n🌦 Condition: {weather_desc.capitalize()}"

def get_top_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()

    if response.get("status") != "ok":
        return "❌ Failed to fetch news!"

    articles = response["articles"][:3]
    news_list = "\n\n".join([f"📰 {a['title']}\n🔗 {a['url']}" for a in articles])
    return f"🌍 **Top News Headlines:**\n\n{news_list}"

def convert_currency(amount, from_currency, to_currency):
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/{from_currency.upper()}"
    response = requests.get(url).json()

    if "conversion_rates" not in response:
        return "❌ Invalid currency code!"

    rate = response["conversion_rates"].get(to_currency.upper())
    if not rate:
        return "❌ Invalid target currency!"

    converted_amount = round(amount * rate, 2)
    return f"💰 {amount} {from_currency.upper()} = {converted_amount} {to_currency.upper()}"

@dp.message(Command("weather"))
async def weather(message: Message):
    city = message.text.split("/weather ", 1)[-1]
    if city == "/weather":
        await message.reply("❗ Please provide a city name. Example: `/weather London`")
        return

    weather_info = get_weather(city)
    await message.reply(weather_info, parse_mode="Markdown")

@dp.message(Command("news"))
async def news(message: Message):
    news_text = get_top_news()
    await message.reply(news_text, parse_mode="Markdown")

@dp.message(Command("convert"))
async def currency(message: Message):
    parts = message.text.split()
    if len(parts) != 4:
        await message.reply("❗ Invalid format! Use: `/convert 100 USD EUR`")
        return

    try:
        amount = float(parts[1])
        from_currency = parts[2].upper()
        to_currency = parts[3].upper()

        conversion_result = convert_currency(amount, from_currency, to_currency)
        await message.reply(conversion_result)
    except ValueError:
        await message.reply("❌ Invalid number format! Example: `/convert 100 USD EUR`")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
