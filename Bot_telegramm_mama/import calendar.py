import calendar
import json
import requests
import telebot
from telebot import types

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx4-fpxBnj2AG8QmgQHqaNTaUoF1-42byl0x3MdKfInRE7MZ7mLjidHAW6zGdPMVGOY/exec"

#bot = telebot.TeleBot('6672306659:AAFlrtezlbtlwz7pKZriivYonqDdR-KsDao')
bot = telebot.TeleBot('6578055244:AAHETS64eT3SslcBN894-wsYwAIoIzW6b1A')
print("Работу начал!Сейчас")

Record = {}
current_step = 0

month_dict = {
    "Январь": "01",
    "Февраль": "02",
    "Март": "03",
    "Апрель": "04",
    "Май": "05",
    "Июнь": "06",
    "Июль": "07",
    "Август": "08",
    "Сентябрь": "09",
    "Октябрь": "10",
    "Ноябрь": "11",
    "Декабрь": "12"
}



        





def choose_option_text(message, options, callback_function):
    markup = types.InlineKeyboardMarkup()

    for i in range(0, len(options), 4):
        row = []
        for j in range(4):
            if i + j < len(options):
                row.append(types.InlineKeyboardButton(options[i + j], callback_data=options[i + j]))

        markup.row(*row)

    markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))

    bot.send_message(message.chat.id, f"Выберите {options[0].lower()}:", reply_markup=markup)
    bot.register_next_step_handler(message, callback_function)


def generate_buttons(options, callback_function):
    markup = types.InlineKeyboardMarkup()

    for i in range(0, len(options), 4):
        row = []
        for j in range(4):
            if i + j < len(options):
                row.append(types.InlineKeyboardButton(options[i + j], callback_data=options[i + j]))

        markup.row(*row)

    markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))
        
    return markup, callback_function


def generate_days_buttons(year, month):
    days_in_month = calendar.monthrange(int(year), int(month))[1]
    return [types.InlineKeyboardButton(str(day), callback_data=f"day_{day}") for day in range(1, days_in_month + 1)]


def generate_time_buttons():
    return [types.InlineKeyboardButton(f"{hour // 2}:{'00' if hour % 2 == 0 else '30'}", callback_data=str(hour)) for
            hour in range(20, 46)]


@bot.message_handler(func=lambda message: any(keyword in message.text.lower() for keyword in
                                              ["выберите год:", "выберите месяц:", "выберите день:",
                                               "выберите время:"]))
@bot.callback_query_handler(func=lambda call: call.message.chat.type == 'private')
def handle_question_message_or_callback(call_or_message):
    if isinstance(call_or_message, telebot.types.Message):
        print("Обработка вопроса:")
        if "год" in call_or_message.text.lower():
            process_year_choice(call_or_message)
        elif "месяц" in call_or_message.text.lower():
            process_month_choice(call_or_message)
        elif "день" in call_or_message.text.lower():
            process_month_day_choice(call_or_message)
        elif "время" in call_or_message.text.lower():
            format_selected_time(call_or_message)
    elif isinstance(call_or_message, telebot.types.CallbackQuery):
        print("Обработка колбэка:")

        if call_or_message.data.isdigit():
            process_year_choice(call_or_message)
        elif call_or_message.data in month_dict:
            process_month_choice(call_or_message)
        elif call_or_message.data.startswith("day_"):
            process_month_day_choice(call_or_message)
        if "время" in call_or_message.message.text.lower():
            format_selected_time(call_or_message)


@bot.message_handler(commands=["start"], func=lambda message: message.chat.type == 'private')
def handle_signup(message):
    global current_step
    current_step = 1

    bot.send_message(message.chat.id, "Пожалуйста, введите ваше имя:")
    bot.register_next_step_handler(message, process_name_step)


def process_name_step(message):
    global current_step
    if current_step == 1:
        name = message.text
        Record["name"] = name
        bot.send_message(message.chat.id, "Введите тему разговора:")
        bot.register_next_step_handler(message, process_topic_step)
        current_step = 2


def process_topic_step(message):
    global current_step
    if current_step == 2:
        topic = message.text
        Record["topic"] = topic
        bot.send_message(message.chat.id, "Введите номер телефона:")
        bot.register_next_step_handler(message, process_phone_step)
        current_step = 3


def process_phone_step(message):
    global current_step
    if current_step == 3:
        phone = message.text
        Record["phone"] = phone
        print("телефон получен")
        print(Record)
        bot.send_message(message.chat.id, "Теперь запланируем удобную дату")
        years = [str(2023), str(2024)]
        markup, callback_function = generate_buttons(years, process_year_choice)
        bot.send_message(message.chat.id, "Выберите год:", reply_markup=markup)
        current_step = 4


def process_year_choice(call):
    global current_step
    if current_step == 4:
        year_choice = call.data
        Record["year"] = year_choice
        print(f"год{call}")
        print(year_choice)
        months = list(month_dict.keys())
        markup, callback_function = generate_buttons(months, process_month_choice)
        bot.send_message(call.message.chat.id, "Выберите месяц:", reply_markup=markup)
        current_step = 5


def process_month_choice(call):
    global current_step
    if current_step == 5:
        month = month_dict[call.data]
        Record["month"] = str(int(month))
        print(f"Выбран месяц {month}")
        print(f"Месяц{call}")
        print(Record)

        days_buttons = generate_days_buttons(Record["year"], month)

        current_step = 6
        markup = types.InlineKeyboardMarkup(row_width=7)
        markup.add(*days_buttons)
        markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))

        bot.send_message(call.message.chat.id, "Выберите день:", reply_markup=markup)


def process_month_day_choice(call):
    print(f"День{call}")
    global current_step
    if current_step == 6:
        day_choice = call.data.replace('day_', '')
        Record["day"] = day_choice
        print(f"выбран день {day_choice}")

        time_buttons = generate_time_buttons()

        current_step = 7
        markup = types.InlineKeyboardMarkup(row_width=4)
        markup.add(*time_buttons)
        markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))

        bot.send_message(call.message.chat.id, "Выберите время:", reply_markup=markup)


def format_selected_time(call):
    time_choice = call.data
    time_text = None

    for row in call.message.json['reply_markup']['inline_keyboard']:
        for button in row:
            if 'callback_data' in button and button['callback_data'] == time_choice:
                time_text = button['text']
                time_choice = time_text
                process_time_choice(call, time_choice)


def process_time_choice(call, time_choice):
    global current_step
    print(time_choice)

    Record["time"] = time_choice
    print("Record['time']:", Record["time"])
    print("Record:", Record)

    process_final_step()
    bot.send_message(call.message.chat.id,
                     f"Заявка на {Record['year']}-{Record['month']}-{Record['day']}-{Record['time']}")


def process_final_step():
    global current_step

    json_data = json.dumps(Record)

    response = requests.post(GOOGLE_SCRIPT_URL, data=json_data)
    if response.status_code == 200:
        print("Данные успешно отправлены")
    else:
        print(f"Ошибка при отправке данных. Код ошибки: {response.status_code}")
    print(json_data)
    print("EnD")

 

@bot.message_handler(commands=["start"])
def say_hi(message):
    print(message)
    if message.chat.type != 'private':
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton('Перейти в личные сообщения', url=f'https://t.me/{bot.get_me().username}?start=private_chat')
        markup.add(btn)
        
        bot.send_message(message.chat.id, "Ссылка на переход в лс бота для записи", reply_markup=markup)

bot.polling(none_stop=True, interval=0)