import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hbold


TOKEN = '6717982152:AAG6Ii59GFng3cJgJ3CYNh5grAe_6H9F01k'
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    builder = InlineKeyboardBuilder()
    show_catalog = InlineKeyboardButton(text='Show catalog', callback_data='show_catalog')
    builder.row(show_catalog)

    hello_text = 'Hello!\nIm Bot - shop with catalog of products!\n\nSee the catalog!'
    try:
        await message.answer(f'{hbold(hello_text)}\n\n'
                             f'Command /start\n'
                             f'Command /help\n', reply_markup=builder.as_markup())

    except TypeError:
        await message.answer('Something gone wrong..')


@dp.message(F.text == '/help')
async def help_handler(message: types.Message):
    builder = InlineKeyboardBuilder()
    button_back = InlineKeyboardButton(text='Back to start', callback_data='back_to_start')
    builder.row(button_back)

    help_text = 'Help section as well..\n\nThis places help information for users.'
    try:
        await message.answer(f'{help_text}', reply_markup=builder.as_markup())

    except TypeError:
        await message.answer('Something gone wrong..')


@dp.callback_query(F.data == 'show_catalog')
async def add_new_func(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    electro_button = InlineKeyboardButton(text='Electro', callback_data='electro_button')
    home_button = InlineKeyboardButton(text='Home', callback_data='home_button')
    button_back = InlineKeyboardButton(text='Back to start', callback_data='back_to_start')
    builder.row(electro_button, home_button)
    builder.row(button_back)

    try:
        await callback.message.answer('Pick the group which you need to see:',
                                      reply_markup=builder.as_markup())

    except TypeError:
        await callback.message.answer('Something gone wrong..')


@dp.callback_query(F.data == 'back_to_start')
async def back_to_start_func(callback: types.CallbackQuery):
    try:
        await start_handler(callback.message)

    except TypeError:
        await callback.message.answer('Something gone wrong..')


async def main():
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print('Exit')
