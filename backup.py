#Scam casino bot, just for educational purposes, so i am not responsible for its use
import os
import random
import re
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
API_TOKEN = 'Insert here yours token'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class Form:
    check_password = 'check_password'
    ask_game_link = 'ask_game_link'

async def remove_language_buttons(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('START!'), KeyboardButton('Выход'))
    await message.reply('Нажимай кнопку START!🚀🍀', reply_markup=keyboard)

async def check_password(message: types.Message):
    if message.text != 'jet100start':
        await message.answer('Неверное кодовое слово, попробуйте еще раз.')
        return False
    else:
        await message.answer('Кодовое слово подтверждено.')
        return True

def is_valid_url(url):
    regex = r'^https:'
    return re.match(regex, url)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Русский'), KeyboardButton('English'))
    await message.answer('Please choose a language:', reply_markup=keyboard)

@dp.message_handler(lambda message: message.text in ['Русский', 'English'], state='*')
async def choose_language(message: types.Message):
    language = message.text
    user_name = message.from_user.first_name
    if message.from_user.last_name:
        user_name += ' ' + message.from_user.last_name
    
    if language == 'Русский':
        await message.reply_photo(open('photos/lucky.jpeg', 'rb'), f'Приветствую тебя в нашей команде, {user_name}! 🚀🍀\n Этот бот даст возможность стабильно зарабатывать каждый день на игре Лаки Джет.\n Все что нужно сделать, это зайти в игру и нажать кнопку ⤵️ СЛЕДУЮЩИЙ СИГНАЛ.\n Бот выдаст коэффициент, а твоя задача сделать ставку и забрать свой первый выигрыш💰')
    else:
        await message.reply_photo(open('photos/lucky.jpeg', 'rb'), f'I welcome you to our team, {user_name}! 🚀🍀\n This bot gives you the opportunity to earn money consistently every day in the Lucky Jet game. All you need to do is go into the game and press the ⤵️ NEXT SIGNAL button. The bot will give you the odds, and your task is to place a bet and collect your first winnings💰')

    await remove_language_buttons(message)

@dp.message_handler(lambda message: message.text == 'START!', state='*')
async def ask_for_password(message: types.Message, state: FSMContext):
    await message.answer('Введите кодовое слово:')
    await state.set_state(Form.check_password)

@dp.message_handler(state=Form.check_password)
async def process_password(message: types.Message, state: FSMContext):
    is_valid_password = await check_password(message)
    if is_valid_password:
        await message.answer('Теперь введите ссылку на игру:')
        await state.set_state(Form.ask_game_link)
    else:
        await ask_for_password(message, state)

@dp.message_handler(state=Form.ask_game_link)
async def process_game_link(message: types.Message, state: FSMContext):
    game_link = message.text
    if is_valid_url(game_link):
        await message.answer('Ссылка на игру принята.')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('Получить коэффициент'), KeyboardButton('Выход'))
        await message.answer('Нажмите "Получить коэффициент" для продолжения.', reply_markup=keyboard)
        await state.finish()
    else:
        await message.answer('Неверный формат ссылки, попробуйте еще раз.')

@dp.message_handler(lambda message: message.text == 'Выход', state='*')
async def restart_bot(message: types.Message):
    await start(message)

@dp.message_handler(lambda message: message.text == 'Получить коэффициент', state='*')
async def send_random_photo(message: types.Message):
    photos_directory = 'photos'
    photo_files = os.listdir(photos_directory)
    random_photo = random.choice(photo_files)
    with open(os.path.join(photos_directory, random_photo), 'rb') as photo:
        await message.answer_photo(photo)

@dp.message_handler()
async def echo_message(message: types.Message):
    await choose_language(message)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
