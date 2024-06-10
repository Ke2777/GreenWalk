import telebot
from telebot import types

bot = telebot.TeleBot('7032527504:AAGRHD975AiIUB8xBzGNWmd3DmVdGrcWPGo')

KeId = 565692562
VeId = 1196997008

KeWalkCount = 0
VeWalkCount = 0

CurrentUserId = 0
SenderId = 0

@bot.message_handler(content_types=['text'])
def start(message):
    global CurrentUserId, SenderId, KeWalkCount, VeWalkCount
    if message.text == '/start':
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        key_ke = types.InlineKeyboardButton(text='Кирилл', callback_data='ke')  # кнопка «Да»
        keyboard.add(key_ke)  # добавляем кнопку в клавиатуру
        key_ve = types.InlineKeyboardButton(text='Вадим', callback_data='ve')
        keyboard.add(key_ve)
        bot.send_message(message.from_user.id, "Привет! С кем я общаюсь?", reply_markup=keyboard)

    if message.text == '/dolg':
        Dolg = KeWalkCount - VeWalkCount
        if Dolg < 0:
            DolgKirilla = Dolg * -1
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
        bot.send_message(message.from_user.id, 'Команды:\n/start - Начало работы\n/dolg - Узнать долг\n/queue - Узнать очередь\n/help - Помощь')

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global CurrentUserId, SenderId, KeWalkCount, VeWalkCount
    if call.data == "ke":  # call.data это callback_data, которую мы указали при объявлении кнопки
        CurrentUserId = KeId
        SenderId = VeId
        bot.send_message(call.message.chat.id, 'Кирилл, привет!')
        WalkCount(call.message)
    elif call.data == "ve":
        CurrentUserId = VeId
        SenderId = KeId
        bot.send_message(call.message.chat.id, 'Вадим, привет!')
        WalkCount(call.message)
    elif call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
        if CurrentUserId == KeId:
            KeWalkCount += 1
            bot.send_message(VeId, "Кирилл погулял с собакой!")
            bot.send_message(KeId, "Молодец!")
        elif CurrentUserId == VeId:
            VeWalkCount += 1
            bot.send_message(KeId, "Вадим погулял с собакой!")
            bot.send_message(VeId, "Молодец!")
    elif call.data == "no":
        bot.send_message(CurrentUserId, 'Лох!')

def WalkCount(message):
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes') # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    bot.send_message(message.chat.id, "Ты гулял с собакой сегодня?", reply_markup=keyboard)

bot.polling(none_stop=True, interval=0)