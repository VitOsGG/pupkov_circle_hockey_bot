from bot import dp
import user
from aiogram.utils import executor

user.register_handlers_user(dp)

executor.start_polling(dp, skip_updates=True)