import random

import telebot

bot = telebot.TeleBot('6672306659:AAFlrtezlbtlwz7pKZriivYonqDdR-KsDao')


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Теперь я с вами, и буду осуждать +- ответ! )')


alternative_responses = [
    "Ты что издеваешься? 😠",
    "Не надо так, пожалуйста. 😡",
    "Серьезно? Это не очень смешно. 😒",
    "Пожалуйста, будьте более уважительны. 🙁",
    "Давай общаться уважительно. 🤐"
]


@bot.message_handler(content_types=["text"])



def handle_text(message):
    message_text = message.text.lower()

    if "+-" in message_text:
        response = random.choice(alternative_responses)
        bot.send_message(message.chat.id, response)

    if "Лена, прекрати" in message_text:
        bot.send_message(message.chat.id, "Лена, сколько можно?🤬")

    if "собраться" in message_text:
        bot.send_message(message.chat.id, "ахахахаха, что за мысли такие?😂😂😂")

    if "работа" in message_text or "работе" in message_text:
        bot.send_message(message.chat.id, "@prezenslimited")

    elif "bot" in message_text or "бот" in message_text:
        bot.send_message(message.chat.id, "только попробуй хуйню сморозить")


bot.polling(none_stop=True, interval=0)
