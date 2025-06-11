
import telebot
from telebot import types

BOT_TOKEN = "7889861772:AAH80YYS3VDQtZEJAQOvGc67npq2IrCxmds"
ADMIN_ID = 7609470280

bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Осинтер")
    btn2 = types.KeyboardButton("Оператор")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Кто ты?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["Осинтер", "Оператор"])
def handle_role(message):
    role = message.text
    user_data[message.chat.id] = {"role": role, "answers": []}
    if role == "Осинтер":
        bot.send_message(message.chat.id, "Какой опыт в осинте?")
    else:
        bot.send_message(message.chat.id, "Какой опыт в ворке?")

@bot.message_handler(func=lambda message: message.chat.id in user_data and len(user_data[message.chat.id]["answers"]) < 3)
def handle_answers(message):
    data = user_data[message.chat.id]
    data["answers"].append(message.text)
    questions = {
        "Осинтер": [
            "Какой опыт в осинте?",
            "Сколько времени готов уделять работе?",
            "Был ли опыт в ворке?"
        ],
        "Оператор": [
            "Какой опыт в ворке?",
            "Сколько времени готов уделять работе?",
            "Откуда узнали о нас?"
        ]
    }

    if len(data["answers"]) < 3:
        next_q = questions[data["role"]][len(data["answers"])]
        bot.send_message(message.chat.id, next_q)
    else:
        summary = f"📥 Новая анкета ({data['role']}):\n"
        for q, a in zip(questions[data["role"]], data["answers"]):
            summary += f"\n❓ {q}\n💬 {a}\n"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ Принять", callback_data=f"accept_{message.chat.id}"))
        markup.add(types.InlineKeyboardButton("❌ Отказать", callback_data=f"reject_{message.chat.id}"))
        bot.send_message(ADMIN_ID, summary, reply_markup=markup)
        bot.send_message(message.chat.id, "Спасибо! Анкета отправлена.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("accept_") or call.data.startswith("reject_"))
def handle_decision(call):
    user_id = int(call.data.split("_")[1])
    if "accept" in call.data:
        bot.send_message(user_id, "🎉 Ваша анкета одобрена!")
        bot.answer_callback_query(call.id, "Принято")
    else:
        bot.send_message(user_id, "❌ Ваша анкета отклонена.")
        bot.answer_callback_query(call.id, "Отклонено")

bot.infinity_polling()
