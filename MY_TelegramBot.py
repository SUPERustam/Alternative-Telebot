import random

from telebot import types
import MY_Tele.config
import telebot

bot = telebot.TeleBot(MY_Tele.config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    ph = open('sticker2.webp', 'rb')  # узнать пол и отправить нужный стикер
    bot.send_sticker(message.chat.id, ph)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 Рандомное число")
    item2 = types.KeyboardButton("😊 Как дела?")
    markup.add(item1, item2)
    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\n<em>{1.first_name}</em> -- бот созданный чтобы быть "
                     "подопытным кроликом.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == '🎲 Рандомное число':
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == '😊 Как дела?':
            mark = types.InlineKeyboardMarkup(row_width=2)
            it1 = types.InlineKeyboardButton("Good", callback_data='good')
            it2 = types.InlineKeyboardButton("Bad", callback_data='bad')
            mark.add(it1, it2)
            bot.send_message(message.chat.id, 'Nice! How are you?', reply_markup=mark)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает 😢')

        # remove inline buttons
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊 Как дела?",
                              reply_markup=None)

        # show alert
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                  text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")


    except Exception as e:
        print(repr(e))


@bot.message_handler(commands=['test'])
def file(message):
    doc = open('graph1.jpeg', 'rb')
    bot.send_document(message.chat.id, doc)


bot.polling(none_stop=True)
