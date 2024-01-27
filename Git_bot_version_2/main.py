import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from bs4 import BeautifulSoup
import requests
from aiogram import types
from config import TOKEN
from aiogram import Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)

dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    user = message.from_user
    greeting_message = f"Привет, {user.full_name}! \n \n Это чат-бот Авроры, который позволит рассчитать стоимость заказа и узнать актуальный курс"
    await message.answer(greeting_message)

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="🕹️Поехали",
        callback_data="Go!")
    )
    await message.answer(
        "Запустите программу: ",
        reply_markup=builder.as_markup()
    )

user_data = {}

def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="Актуальный курс", callback_data="rate", resize_keyboard=True),
            types.InlineKeyboardButton(text="Рассчитать заказ", callback_data="rate_order", resize_keyboard=True),
            types.InlineKeyboardButton(text="Справка с вопросами", callback_data="qiuestions", resize_keyboard=True),
            types.InlineKeyboardButton(text="Поддержка", callback_data="support", resize_keyboard=True)
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def get_rate():
    url = "https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D1%8E%D0%B0%D0%BD%D1%8F+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=rehc+%2Ffyz+r+&gs_lcrp=EgZjaHJvbWUqCggBEAAYChgWGB4yBggAEEUYOTIKCAEQABgKGBYYHjIKCAIQABgKGBYYHjIKCAMQABgKGBYYHjIKCAQQABgKGBYYHjIICAUQABgWGB4yCggGEAAYChgWGB4yCggHEAAYChgWGB4yCggIEAAYChgWGB4yCggJEAAYChgWGB7SAQgzNDk3ajFqN6gCALACAA&sourceid=chrome&ie=UTF-8"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            result = soup.find("div", class_="BNeawe iBp4i AP7Wnd")
            if result:
                return result.text
    except Exception as e:
        return "Ошибка при получении курса"
    

async def calculate_rate(message: types.Message = None):
    try:
        if message:
            await message.reply("Привет! Введите число для умножения на курс")
            return
        
        user_number = float(message.text)
        url = "https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D1%8E%D0%B0%D0%BD%D1%8F+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=rehc+%2Ffyz+r+&gs_lcrp=EgZjaHJvbWUqCggBEAAYChgWGB4yBggAEEUYOTIKCAEQABgKGBYYHjIKCAIQABgKGBYYHjIKCAMQABgKGBYYHjIKCAQQABgKGBYYHjIICAUQABgWGB4yCggGEAAYChgWGB4yCggHEAAYChgWGB4yCggIEAAYChgWGB4yCggJEAAYChgWGB7SAQgzNDk3ajFqN6gCALACAA&sourceid=chrome&ie=UTF-8"
        
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            result = soup.find("div", class_="BNeawe iBp4i AP7Wnd")
            if result:
                rate = float(result.text.split()[0].replace(',', '.')) + 1
                result = user_number * rate
                return f"Ответ: {result}"
        else:
            return "Ошибка при получении данных"
    except ValueError:
        return "Пожалуйста, введите число."


@dp.message(Command("rate_order"))
async def process_rate_order(message: types.Message):
    response = await calculate_rate(message)
    await message.reply(response)

     

@dp.callback_query(F.data == "Go!")
async def second_choose_character(callback: types.CallbackQuery):
    await callback.message.answer("Выберите действие:", reply_markup=get_keyboard())
    return



@dp.callback_query(F.data == "rate")
async def cmd_rate(callback: types.CallbackQuery):
    rate = await get_rate()
    rate = float(rate.split()[0].replace(',', '.')) + 1
    rate_type = type(rate)
    await callback.message.answer(f" Курс юаня к рублю: {rate}")
    return


@dp.callback_query(F.data == "support")
async def cmd_rate(callback: types.CallbackQuery):
    await callback.message.answer("Поддержка")
    return

@dp.callback_query(F.data == "rate_order")
async def rate_and_plus(callback: types.CallbackQuery):
    await callback.message.answer(" ")
    return




async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())