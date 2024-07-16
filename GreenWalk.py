import telebot
from telebot import types
import json
import time

bot = telebot.TeleBot('7032527504:AAGRHD975AiIUB8xBzGNWmd3DmVdGrcWPGo')

KeId = 565692562
VeId = 1196997008

data_file = 'walk_data.json'


# Загрузка данных из файла
def load_data():
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {'KeWalkCount': 0, 'VeWalkCount': 0}


# Сохранение данных в файл
def save_data(data):
    with open(data_file, 'w') as f:
        json.dump(data, f)


data = load_data()
KeWalkCount = data['KeWalkCount']
VeWalkCount = data['VeWalkCount']

CurrentUserId = 0
SenderId = 0


@bot.message_handler(content_types=['text'])
def start(message):
    global CurrentUserId, SenderId, KeWalkCount, VeWalkCount
    if message.text == '/start':
        keyboard = types.InlineKeyboardMarkup()
        key_ke = types.InlineKeyboardButton(text='Кирилл', callback_data='ke')
        keyboard.add(key_ke)
        key_ve = types.InlineKeyboardButton(text='Вадим', callback_data='ve')
        keyboard.add(key_ve)
        bot.send_message(message.from_user.id, "Привет! С кем я общаюсь?", reply_markup=keyboard)

    if message.text == '/dolg':
        Dolg = KeWalkCount - VeWalkCount
        if Dolg < 0:
            DolgKirilla = -Dolg
            bot.send_message(message.from_user.id, f'Долг Кирилла: {DolgKirilla}')
        elif Dolg > 0:
            DolgVadima = Dolg
            bot.send_message(message.from_user.id, f'Долг Вадима: {DolgVadima}')
        else:
            bot.send_message(message.from_user.id, 'Нет долгов!')

    if message.text == '/queue':
        Dolg = KeWalkCount - VeWalkCount
        if Dolg < 0:
            bot.send_message(message.from_user.id, 'Очередь Кирилла!')
        elif Dolg > 0:
            bot.send_message(message.from_user.id, 'Очередь Вадима!')
        else:
            bot.send_message(message.from_user.id, 'Очередь еще не началась!')

    if message.text == '/help':
        bot.send_message(message.from_user.id,
                         'Команды:\n/start - Начало работы\n/dolg - Узнать долг\n/queue - Узнать очередь\n/help - Помощь')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global CurrentUserId, SenderId, KeWalkCount, VeWalkCount
    if call.data == "ke":
        CurrentUserId = KeId
        SenderId = VeId
        bot.send_message(call.message.chat.id, 'Кирилл, привет!')
        WalkCount(call.message)
    elif call.data == "ve":
        CurrentUserId = VeId
        SenderId = KeId
        bot.send_message(call.message.chat.id, 'Вадим, привет!')
        WalkCount(call.message)
    elif call.data == "yes":
        if CurrentUserId == KeId:
            KeWalkCount += 1
            bot.send_message(VeId, "Кирилл погулял с собакой!")
            bot.send_message(KeId, "Молодец!")
        elif CurrentUserId == VeId:
            VeWalkCount += 1
            bot.send_message(KeId, "Вадим погулял с собакой!")
            bot.send_message(VeId, "Молодец!")

        # Переключаем очередь, если долг стал нулевым
        Dolg = KeWalkCount - VeWalkCount
        if Dolg == 0:
            if CurrentUserId == KeId:
                VeWalkCount += 1
                bot.send_message(KeId, "Теперь очередь Вадима!")
                bot.send_message(VeId, "Теперь твоя очередь!")
            elif CurrentUserId == VeId:
                KeWalkCount += 1
                bot.send_message(VeId, "Теперь очередь Кирилла!")
                bot.send_message(KeId, "Теперь твоя очередь!")
        save_data({'KeWalkCount': KeWalkCount, 'VeWalkCount': VeWalkCount})
    elif call.data == "no":
        bot.send_message(CurrentUserId, 'Лох!')


def WalkCount(message):
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    bot.send_message(message.chat.id, "Ты гулял с собакой сегодня?", reply_markup=keyboard)


while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(15)  # Wait 15 seconds before restarting the bot