import telebot
import random
from flask import Flask, request

TOKEN = '8036017301:AAGuK4bnXaY3zosVs8FDFnJFVZU0kp47qXQ'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Список офферов
offers = [
    "https://lnk.do/x8H2aVwb",
    "https://lnk.do/FeVFAh5"
]

# Храним, какие офферы уже были показаны каждому пользователю
user_offers = {}

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_offers[user_id] = []
    welcome = (
        "👋 Добро пожаловать в *KiCheckBot!*\n\n"
        "🔍 Проверьте свою кредитную историю и получите одобрение на займ "
        "от проверенных МФО.\n\n"
        "Нажмите кнопку ниже, чтобы начать:"
    )
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📊 Проверить КИ")
    bot.send_message(user_id, welcome, reply_markup=markup, parse_mode="Markdown")

# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    text = message.text.lower()

    if user_id not in user_offers:
        user_offers[user_id] = []

    if "проверить ки" in text:
        send_offer(user_id)
    elif "ещё вариант" in text:
        send_offer(user_id)
    else:
        bot.send_message(user_id, "Выберите действие с помощью кнопок ниже.")

def send_offer(user_id):
    shown = user_offers.get(user_id, [])
    remaining = list(set(offers) - set(shown))

    if not remaining:
        user_offers[user_id] = []
        remaining = offers.copy()

    offer = random.choice(remaining)
    user_offers[user_id].append(offer)

    msg = (
        "💳 Вот один из вариантов микрозайма для вас:\n"
        f"{offer}\n\n"
        "Если не подошло — нажмите «Ещё вариант»."
    )
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔁 Ещё вариант")
    bot.send_message(user_id, msg, reply_markup=markup)

# Webhook обработка
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route('/', methods=['GET'])
def index():
    return 'Bot is running!', 200

if __name__ == '__main__':
    import os
    bot.remove_webhook()
    bot.set_webhook(url=f"https://tg-bot-mfo.onrender.com/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
