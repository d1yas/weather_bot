import logging
import requests
import datetime
from config import API_TOKEN, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Salom! Menga shahar nomini yozing, men sizga ob-havo hisobotini yuboraman!")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Quyoshli \U00002600",
        "Clouds": "Bulutli \U00002601",
        "Rain": "Yomgir \U00002614",
        "Drizzle": "Kuchli yomgir \U00002614",
        "Thunderstorm": "Mamoqaldiroq \U000026A1",
        "Snow": "Qor \U0001F328",
        "Mist": "Tuman \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Ob-havo aniqlanmadi!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Shahardagi Ob-havo: {city}\nTemperatura: {cur_weather}C° {wd}\n"
              f"Namlik: {humidity}%\nBosim: {pressure} мм.рт.ст\nShamol tezligi: {wind} м/с\n"
              f"Quyosh chiqishi: {sunrise_timestamp}\nQuyosh botishi: {sunset_timestamp}\nKunning uzunligi: {length_of_the_day}\n"
              f"***Hayrli kun!***"
              )

    except:
        await message.reply("\U00002620 Shahar nomini tekshiring \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)