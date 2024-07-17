import telebot
from telebot import types
import json
import time
import schedule
import threading

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

user_chats = {KeId: None, VeId: None}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.from_user.id in [KeId, VeId]:
        user_chats[message.from_user.id] = message.chat.id
        bot.send_message(message.chat.id, "Привет! Напиши /help для списка доступных команд.")
        send_main_menu(message.chat.id)
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к этому боту.")


def send_main_menu(chat_id):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_walk = types.KeyboardButton('/walk')
    btn_dolg = types.KeyboardButton('/dolg')
    btn_queue = types.KeyboardButton('/queue')
    btn_help = types.KeyboardButton('/help')
    keyboard.add(btn_walk, btn_dolg, btn_queue, btn_help)
    bot.send_message(chat_id, "Выберите команду:", reply_markup=keyboard)


@bot.message_handler(commands=['dolg'])
def send_dolg(message):
    Dolg = KeWalkCount - VeWalkCount
    if Dolg < 0:
        DolgKirilla = -Dolg
        bot.send_message(message.from_user.id, f'Долг Кирилла: {DolgKirilla}')
    elif Dolg > 0:
        DolgVadima = Dolg
        bot.send_message(message.from_user.id, f'Долг Вадима: {DolgVadima}')
    else:
        bot.send_message(message.from_user.id, 'Нет долгов!')


@bot.message_handler(commands=['queue'])
def send_queue(message):
    Dolg = KeWalkCount - VeWalkCount
    if Dolg < 0:
        bot.send_message(message.from_user.id, 'Очередь Кирилла!')
    elif Dolg > 0:
        bot.send_message(message.from_user.id, 'Очередь Вадима!')
    else:
        bot.send_message(message.from_user.id, 'Очередь еще не началась!')


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.from_user.id,
                     'Команды:\n/start - Начало работы\n/dolg - Узнать долг\n/queue - Узнать очередь\n/help - Помощь\n/admin - Админ панель (только для Кирилла)')


@bot.message_handler(commands=['admin'])
def send_admin(message):
    if message.from_user.id == KeId:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Увеличить долг Кирилла')
        btn2 = types.KeyboardButton('Уменьшить долг Кирилла')
        btn3 = types.KeyboardButton('Увеличить долг Вадима')
        btn4 = types.KeyboardButton('Уменьшить долг Вадима')
        btn5 = types.KeyboardButton('Закрыть админ панель')
        keyboard.add(btn1, btn2)
        keyboard.add(btn3, btn4)
        keyboard.add(btn5)
        bot.send_message(message.chat.id, "Админ панель:", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к админ панели.")


@bot.message_handler(
    func=lambda message: message.text in ['Увеличить долг Кирилла', 'Уменьшить долг Кирилла', 'Увеличить долг Вадима',
                                          'Уменьшить долг Вадима', 'Закрыть админ панель'])
def admin_panel(message):
    global KeWalkCount, VeWalkCount
    if message.from_user.id == KeId:
        if message.text == 'Увеличить долг Кирилла':
            VeWalkCount += 1
        elif message.text == 'Уменьшить долг Кирилла':
            VeWalkCount -= 1
        elif message.text == 'Увеличить долг Вадима':
            KeWalkCount += 1
        elif message.text == 'Уменьшить долг Вадима':
            KeWalkCount -= 1
        elif message.text == 'Закрыть админ панель':
            bot.send_message(message.chat.id, "Админ панель закрыта.", reply_markup=types.ReplyKeyboardRemove())
            send_main_menu(message.chat.id)
            return
        save_data({'KeWalkCount': KeWalkCount, 'VeWalkCount': VeWalkCount})
        bot.send_message(message.chat.id, "Долги обновлены.")
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к админ панели.")


@bot.message_handler(commands=['walk'])
def walk(message):
    if message.from_user.id in [KeId, VeId]:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_yes = types.KeyboardButton('Да')
        key_no = types.KeyboardButton('Нет')
        keyboard.add(key_yes, key_no)
        bot.send_message(message.chat.id, "Ты гулял с собакой сегодня?", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к этому боту.")


@bot.message_handler(func=lambda message: message.text in ['Да', 'Нет'])
def handle_walk_response(message):
    global KeWalkCount, VeWalkCount, KeId, VeId
    if message.from_user.id in [KeId, VeId]:
        if message.text == 'Да':
            if message.from_user.id == KeId:
                KeWalkCount += 1
                if user_chats[VeId]:
                    bot.send_message(user_chats[VeId], "Кирилл погулял с собакой!")
                bot.send_message(user_chats[KeId], "Молодец!")
            elif message.from_user.id == VeId:
                VeWalkCount += 1
                if user_chats[KeId]:
                    bot.send_message(user_chats[KeId], "Вадим погулял с собакой!")
                bot.send_message(user_chats[VeId], "Молодец!")

            Dolg = KeWalkCount - VeWalkCount
            if Dolg == 0:
                if message.from_user.id == KeId:
                    VeWalkCount += 1
                    bot.send_message(user_chats[KeId], "Теперь очередь Вадима!")
                    bot.send_message(user_chats[VeId], "Теперь твоя очередь!")
                elif message.from_user.id == VeId:
                    KeWalkCount += 1
                    bot.send_message(user_chats[VeId], "Теперь очередь Кирилла!")
                    bot.send_message(user_chats[KeId], "Теперь твоя очередь!")
            save_data({'KeWalkCount': KeWalkCount, 'VeWalkCount': VeWalkCount})
            send_main_menu(message.chat.id)
        elif message.text == 'Нет':
            bot.send_message(message.chat.id, 'Лох!')
            send_main_menu(message.chat.id)
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к этому боту.")


def send_daily_reminder():
    Dolg = KeWalkCount - VeWalkCount
    if Dolg < 0:
        bot.send_message(user_chats[KeId], "Не забудь что сегодня твоя очередь гулять с собакой!!!")
    elif Dolg > 0:
        bot.send_message(user_chats[VeId], "Не забудь что сегодня твоя очередь гулять с собакой!!!")
    else:
        # In case there's no debt, we can send a general reminder
        if user_chats[KeId]:
            bot.send_message(user_chats[KeId], "Не забудь что сегодня твоя очередь гулять с собакой!!!")
        if user_chats[VeId]:
            bot.send_message(user_chats[VeId], "Не забудь что сегодня твоя очередь гулять с собакой!!!")


def schedule_daily_reminders():
    schedule.every().day.at("19:00").do(send_daily_reminder)
    while True:
        schedule.run_pending()
        time.sleep(1)


# Run the scheduler in a separate thread
threading.Thread(target=schedule_daily_reminders).start()

while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(15)  # Wait 15 seconds before restarting the bot