import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hbold

from db_conn import session, User
from products import apple_laptops, windows_laptops


TOKEN = '**********************'
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    try:
        user = session.query(User).filter_by(user_id=user_id).first()
        if not user and message.from_user.first_name != 'Aiogram_test':
            user = User(user_id=user_id, first_name=message.from_user.first_name, last_name=message.from_user.last_name,
                        full_name=message.from_user.full_name, user_name=message.from_user.username,
                        language_code=message.from_user.language_code)
            try:
                session.add(user)
                session.commit()

            except ConnectionError:
                await message.answer('DB ERROR. USER DON`T ADD. TRY AGAIN.')

    except ConnectionError:
        await message.answer('DB ERROR. USER DON`T SELECTED. TRY AGAIN.')

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
async def show_catalog_func(callback: types.CallbackQuery):
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


@dp.callback_query(F.data == 'electro_button')
async def electro_func(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    smartphones_button = InlineKeyboardButton(text='Smartphones', callback_data='smartphones_button')
    laptops_button = InlineKeyboardButton(text='Laptops', callback_data='laptops_button')
    button_back = InlineKeyboardButton(text='Back to start', callback_data='back_to_start')
    builder.row(smartphones_button, laptops_button)
    builder.row(button_back)

    try:
        await callback.message.answer('Pick the category which you need:',
                                      reply_markup=builder.as_markup())

    except TypeError:
        await callback.message.answer('Something gone wrong..')


@dp.callback_query(F.data == 'smartphones_button')
async def smartphones_func(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    apple_smartphones_button = InlineKeyboardButton(text='Apple', callback_data='apple_smartphones_button')
    android_smartphones_button = InlineKeyboardButton(text='Android', callback_data='android_smartphones_button')
    button_back = InlineKeyboardButton(text='Back to start', callback_data='back_to_start')
    builder.row(apple_smartphones_button, android_smartphones_button)
    builder.row(button_back)

    try:
        await callback.message.answer('Pick the category which you need:',
                                      reply_markup=builder.as_markup())

    except TypeError:
        await callback.message.answer('Something gone wrong..')


@dp.callback_query(F.data == 'laptops_button')
async def laptops_func(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    apple_laptops_button = InlineKeyboardButton(text='Mac OS', callback_data='apple_laptops_button')
    windows_laptops_button = InlineKeyboardButton(text='Windows', callback_data='windows_laptops_button')
    button_back = InlineKeyboardButton(text='Back to start', callback_data='back_to_start')
    builder.row(apple_laptops_button, windows_laptops_button)
    builder.row(button_back)

    try:
        await callback.message.answer('Pick the category which you need:',
                                      reply_markup=builder.as_markup())

    except TypeError:
        await callback.message.answer('Something gone wrong..')


@dp.callback_query(F.data == 'apple_laptops_button')
async def apple_laptops_func(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()

    products_buttons = []
    for name, desc_price in apple_laptops.items():
        products_buttons.append(InlineKeyboardButton(text=f'{list(apple_laptops.keys()).index(name) + 1} | {name} | {desc_price[1]}', callback_data=f'{name}'))

    button_back = InlineKeyboardButton(text='Back to start', callback_data='back_to_start')

    for i in products_buttons:
        builder.row(i)

    builder.row(button_back)

    try:
        await callback.message.answer('Pick the product which you need:',
                                      reply_markup=builder.as_markup())

    except TypeError:
        await callback.message.answer('Something gone wrong..')


@dp.callback_query(F.data == 'windows_laptops_button')
async def windows_laptops_func(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()

    products_buttons = []
    for name, desc_price in windows_laptops.items():
        products_buttons.append(InlineKeyboardButton(text=f'{list(windows_laptops.keys()).index(name) + 1} | {name} | {desc_price[1]}', callback_data=f'{name}'))

    button_back = InlineKeyboardButton(text='Back to start', callback_data='back_to_start')

    for i in products_buttons:
        builder.row(i)

    builder.row(button_back)

    try:
        await callback.message.answer('Pick the product which you need:',
                                      reply_markup=builder.as_markup())

    except TypeError:
        await callback.message.answer('Something gone wrong..')


@dp.callback_query(lambda callback: callback.data in apple_laptops.keys() or callback.data in windows_laptops.keys())
async def product_desc_func(callback: types.CallbackQuery):
    product_name = callback.data
    product_desc = apple_laptops[callback.data][0] if callback.data in apple_laptops.keys() else windows_laptops[callback.data][0]
    product_price = apple_laptops[callback.data][1] if callback.data in apple_laptops.keys() else windows_laptops[callback.data][1]

    builder = InlineKeyboardBuilder()
    buy_it_button = InlineKeyboardButton(text='Buy it', callback_data=f'{product_name}')
    button_back = InlineKeyboardButton(text='Back to start', callback_data='back_to_start')
    builder.row(buy_it_button)
    builder.row(button_back)

    try:
        await callback.message.answer(f'Description of product:\n\n'
                                      f'{product_name}\n'
                                      f'{product_desc}\n\n'
                                      f'{product_price} $',
                                      reply_markup=builder.as_markup())

    except TypeError:
        await callback.message.answer('Something gone wrong..')


@dp.callback_query(F.data == 'home_button')
async def home_func(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    furniture_button = InlineKeyboardButton(text='Furniture', callback_data='furniture_button')
    bathroom_button = InlineKeyboardButton(text='Bathroom', callback_data='bathroom_button')
    button_back = InlineKeyboardButton(text='Back to start', callback_data='back_to_start')
    builder.row(furniture_button, bathroom_button)
    builder.row(button_back)

    try:
        await callback.message.answer('Pick the category which you need:',
                                      reply_markup=builder.as_markup())

    except TypeError:
        await callback.message.answer('Something gone wrong..')


@dp.callback_query(F.data == 'furniture_button')
async def furniture_func(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    chairs_button = InlineKeyboardButton(text='Chairs', callback_data='chairs_button')
    beds_button = InlineKeyboardButton(text='Beds', callback_data='beds_button')
    button_back = InlineKeyboardButton(text='Back to start', callback_data='back_to_start')
    builder.row(chairs_button, beds_button)
    builder.row(button_back)

    try:
        await callback.message.answer('Pick the category which you need:',
                                      reply_markup=builder.as_markup())

    except TypeError:
        await callback.message.answer('Something gone wrong..')


@dp.callback_query(F.data == 'bathroom_button')
async def bathroom_func(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    toilets_button = InlineKeyboardButton(text='Toilets', callback_data='toilets_button')
    shower_cabins_button = InlineKeyboardButton(text='Shower cabins', callback_data='shower_cabins_button')
    button_back = InlineKeyboardButton(text='Back to start', callback_data='back_to_start')
    builder.row(toilets_button, shower_cabins_button)
    builder.row(button_back)

    try:
        await callback.message.answer('Pick the category which you need:',
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
