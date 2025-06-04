import telebot
import random

TOKEN = "8036017301:AAGuK4bnXaY3zosVs8FDFnJFVZU0kp47qXQ"
bot = telebot.TeleBot(TOKEN)

offers = [
    "https://lnk.do/x8H2aVwb",
    "https://lnk.do/FeVFAh5"
]

user_sessions = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_sessions[user_id] = {"shown": []}
    bot.send_message(user_id, "👋 Добро пожаловать в KiCheckBot!
Проверьте свою кредитную историю и получите одобрение.")
    show_offer(message)

def show_offer(message):
    user_id = message.chat.id
    shown = user_sessions[user_id]["shown"]
    remaining = [offer for offer in offers if offer not in shown]

    if not remaining:
        user_sessions[user_id]["shown"] = []
        remaining = offers.copy()

    offer = random.choice(remaining)
    user_sessions[user_id]["shown"].append(offer)

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("💰 Перейти к офферу", url=offer))
    markup.add(telebot.types.InlineKeyboardButton("🔁 Получить другой оффер", callback_data="next_offer"))
    bot.send_message(user_id, "Вот предложение для вас:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "next_offer")
def callback_next_offer(call):
    show_offer(call.message)

bot.polling()
