from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os


# Использование переменной окружения TOKEN
TOKEN = os.environ.get("TOKEN")

# Инициализация хранилища состояний
storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
