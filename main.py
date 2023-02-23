import telebot
from telebot import types
from questions import statements, correct_answers, welcome_message
from TOKEN import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Start quizz")
    markup.add(btn1)
    bot.send_message(message.from_user.id, welcome_message, reply_markup=markup)


question_counter = 1
user_answers = {}


@bot.message_handler(content_types=['text'])
def get_menu(message):
    global question_counter, user_answers

    if message.text == 'Start quizz':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Propaganda")
        btn2 = types.KeyboardButton("Nu e propaganda")
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, statements['q1'], reply_markup=markup)

    elif message.text in ["Propaganda", "Nu e propaganda"]:
        # Store the user's answer
        user_answers[f'q{question_counter}'] = message.text

        if question_counter == len(statements):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Correct answers")
            markup.add(btn1)
            bot.send_message(message.from_user.id, f"Quizz is over. Your answers: ", reply_markup=markup)
            for question, answer in user_answers.items():
                bot.send_message(message.from_user.id, f"{question}: {answer}")

        else:
            question_counter += 1
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Propaganda")
            btn2 = types.KeyboardButton("Nu e propaganda")
            markup.add(btn1, btn2)
            bot.send_message(message.from_user.id, statements[f'q{question_counter}'], reply_markup=markup)

    elif message.text == 'Correct answers':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Thanks")
        markup.add(btn1)
        bot.send_message(message.from_user.id, f"Correct answers are: ", reply_markup=markup)
        for k, v in correct_answers.items():
            bot.send_message(message.from_user.id, f"{k}: {v}")


bot.polling(none_stop=True, interval=0)
