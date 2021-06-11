import MY_Tele.config
import logging

from aiogram import Bot, Dispatcher, executor, types
from MY_Tele.SQLite_for_TelegramBot_v2 import SQLighter

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

bot = Bot(token=MY_Tele.config.TOKEN)
dp = Dispatcher(bot)

# initialize connection to database
db = SQLighter('db.db')


# command to active subscription
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # if user not in database, we add him
        db.add_subscriber(message.from_user.id)
    else:
        # if user in database, we subscribe him
        db.update_subscription(message.from_user.id, True)

    await message.answer('вы успешно подписались на рассылку\nУдачи!')


# command to unsubscribe user
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # if user not in database, we add him with inactive subscription()
        db.add_subscriber(message.from_user.id, False)
        await message.answer("Вы не подписаны.")
    else:
        # if user in database, we subscribe him
        db.update_subscription(message.from_user.id, False)
        await message.answer('вы успешно отписались от рассылки:(')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
