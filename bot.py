import telebot
from telebot import types
import info

# Создаем бота
bot = telebot.TeleBot('6363172638:AAGaTWfxpBZtwJVV7uGvTY2nE_wG_8otCzA')
keyboard_yes_or_no = types.ReplyKeyboardMarkup(row_width=2)
button_yes = types.KeyboardButton('Да')
button_no = types.KeyboardButton('Нет')
keyboard_yes_or_no.add(button_yes, button_no)

keyboard_start = types.ReplyKeyboardMarkup(row_width=1)
keyboard_start.add(types.KeyboardButton("/start"))


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Приветственное сообщение и предложение пройти опрос
    bot.send_message(message.chat.id,
                     "Привет! Я помогу тебе проверить, насколько ты знаешь столицы стран мира. Готов начать?")
    info.init_user_data(message.chat.id)
    # Отправляем клавиатуру пользователю
    bot.send_message(message.chat.id, "Выбери один из вариантов:", reply_markup=keyboard_yes_or_no)


# Обработчик ответа на вопрос о начале опроса
@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    current_user_data = info.get_user_data(message.chat.id)

    if current_user_data["current_step"] is None:
        if message.text.lower() == "да":
            bot.send_message(message.chat.id, "Отлично! Давай начнем.")
            question = info.get_current_question(message.chat.id)
            updated_user_data = info.get_user_data(message.chat.id)
            updated_user_data["current_step"] = 1
            info.update_user_data(message.chat.id, updated_user_data)
            bot.send_message(message.chat.id, question,
                             reply_markup=types.ReplyKeyboardRemove())
        elif message.text.lower() == "нет":
            bot.send_message(message.chat.id, "Возвращайся скорее!", reply_markup=keyboard_start)

    elif current_user_data["current_step"] < 10:
        info.check_answer(message.chat.id, message.text)
        question = info.get_current_question(message.chat.id)
        updated_user_data = info.get_user_data(message.chat.id)
        updated_user_data["current_step"] += 1
        info.update_user_data(message.chat.id, updated_user_data)
        bot.send_message(message.chat.id, question,
                         reply_markup=types.ReplyKeyboardRemove())

    elif current_user_data["current_step"] == 10:
        info.check_answer(message.chat.id, message.text)
        result_score = info.get_user_score(message.chat.id)
        bot.send_message(message.chat.id, result_score)
        updated_user_data = info.get_user_data(message.chat.id)
        updated_user_data["current_step"] += 1
        updated_user_data["score"] = 0
        bot.send_message(message.chat.id, "Хочешь начать заново?", reply_markup=keyboard_yes_or_no)

    elif current_user_data["current_step"] == 11:
        if message.text.lower() == "да":
            question = info.get_current_question(message.chat.id)
            updated_user_data = info.get_user_data(message.chat.id)
            updated_user_data["current_step"] = 1
            bot.send_message(message.chat.id, question, reply_markup=types.ReplyKeyboardRemove())
        elif message.text.lower() == "нет":
            bot.send_message(message.chat.id, "Возвращайся скорее!", reply_markup=keyboard_start)


# Запускаем бота
bot.infinity_polling()
