from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Использование переменной окружения TOKEN
TOKEN = os.getenv("TOKEN")
print(TOKEN)

# Инициализация хранилища состояний
storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
CHANNEL_ID = os.getenv("CHANNEL_ID")