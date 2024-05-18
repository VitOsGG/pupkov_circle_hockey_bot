from bot import bot, dp
from aiogram import types
# from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from generate_imag import image_khl, image_nhl
from keybord import kb_user
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import random
import os
from dotenv import load_dotenv
import logging

# Инициализация логгера
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())

# Объект для извлечения переменных
load_dotenv()

# Айди чата куда необходимо отправлять картинки
CHANNEL_ID = os.getenv('CHANNEL_ID')

# Ваш user ID
ALLOWED_USER_ID = os.getenv('ALLOWED_USER_ID')


# Проверка доступа к боту
def restricted(handler):
    async def wrapper(message: types.Message):
        user_id = str(message.from_user.id)
        if user_id != ALLOWED_USER_ID:
            await message.reply("Это приватный бот")
            logging.warning(f"Попытка доступа к боту от пользователя: {user_id}.")
            return
        else:
            return await handler(message)
    return wrapper

# Обработчик команды /start
@restricted
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "Привет!\nНадо выбрать лигу!", reply_markup=kb_user)
    except:
        await message.reply('Хоккейные новости и не только..! Подпишись: \nhttps://t.me/pupkoviktor')


def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help', 'Start', 'Help'])


qustions_list = ['Как вам результаты', 'Ваша команда победила', 'Ожидаемо']


async def post_image_to_channel(image):
    with open(image, 'rb') as photo:
        random_question = random.choice(qustions_list)+"❓"+'\n.\n.\n.\n@pupkoviktor'
        await bot.send_photo(chat_id=CHANNEL_ID, photo=photo, caption=random_question)


# ДЛЯ !!!КХЛ!!!
# Определение состояний
class KHLState(StatesGroup):
    Teams = State()
    Results = State()


# Обработчик для команды "КХЛ"
@dp.message_handler(Text(equals="КХЛ"))
async def khl_select(message: types.Message):
    # Переход к следующему состоянию - ожиданию списка команд
    await KHLState.Teams.set()
    await bot.send_message(message.from_user.id, 'Введите список команд через запятую:')


# Обработчик для ввода списка команд
@dp.message_handler(state=KHLState.Teams)
async def process_teams(message: types.Message, state: FSMContext):
    teams_input = message.text.replace(', ', ',').split(',')
    print(teams_input)
    # Сохраняем список команд в контексте
    await state.update_data(teams=teams_input)
    # Переход к следующему состоянию - ожиданию списка результатов
    await KHLState.Results.set()
    await message.answer('Теперь введите список результатов через запятую:')


# Ваш код обработчика для результатов
@dp.message_handler(state=KHLState.Results)
async def process_results(message: types.Message, state: FSMContext):
    results_input = message.text.replace(', ', ',').split(',')
    print(results_input)
    data = await state.get_data()
    teams = data.get('teams')

    try:
        image = image_khl(teams, results_input)
        with open(image, 'rb') as photo:
            await bot.send_photo(message.from_user.id, photo)
        await post_image_to_channel(image)
    except ValueError as e:
        print(f"Ошибка: {e}")
        register_handlers_user(dp)

    await KHLState.Teams.set()
    await state.reset_state()


# !!!ДЛЯ НХЛ!!!
# Определение состояний
class NHLState(StatesGroup):
    Teams = State()
    Results = State()


# Обработчик для команды "НХЛ"
@dp.message_handler(Text(equals="НХЛ"))
async def nhl_select(message: types.Message):
    await bot.send_message(message.from_user.id, 'Введите список команд через запятую:')
    # Переход к следующему состоянию - ожиданию списка команд
    await NHLState.Teams.set()


# Обработчик для ввода списка команд
@dp.message_handler(state=NHLState.Teams)
async def process_teams(message: types.Message, state: FSMContext):
    teams_input = message.text.replace(', ', ',').split(',')
    print(teams_input)
    # Сохраняем список команд в контексте
    await state.update_data(teams=teams_input)
    await message.answer('Теперь введите список результатов через запятую:')

    # Переход к следующему состоянию - ожиданию списка результатов
    await NHLState.Results.set()


# Обработчик для ввода списка результатов
@dp.message_handler(state=NHLState.Results)
async def process_results(message: types.Message, state: FSMContext):
    results_input = message.text.replace(', ', ',').split(',')
    print(results_input)
    # Получаем список команд из контекста
    data = await state.get_data()
    teams = data.get('teams')

    try:
        image = image_nhl(teams, results_input)
        with open(image, 'rb') as photo:
            await bot.send_photo(message.from_user.id, photo)
        await post_image_to_channel(image)
    except ValueError as e:
        print(f"Ошибка: {e}")
        register_handlers_user(dp)

    # Возвращаемся в начальное состояние
    await NHLState.Teams.set()
    # Очищаем контекст
    await state.reset_state()

