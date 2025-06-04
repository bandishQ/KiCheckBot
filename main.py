import telebot
from flask import Flask, request

API_TOKEN = '8036017301:AAGuK4bnXaY3zosVs8FDFnJFVZU0kp47qXQ'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

offers = [
    "🔥 <a href='https://lnk.do/x8H2aVwb'>Узнать свой рейтинг и получить займ</a>",
    "💰 <a href='https://lnk.do/FeVFAh5'>Моментальное одобрение займа</a>"
]

user_data = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.chat.id
    user_data[user_id] = {'step': 1}
    bot.send_message(user_id, "👋 Добро пожаловать в <b>KiCheckBot</b>!\n\n"
                              "Проверьте свою кредитную историю и получите одобрение на займ.", parse_mode='HTML')
    bot.send_message(user_id, "📞 Пожалуйста, отправьте ваш номер телефона для продолжения.")

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    user_id = message.chat.id
    user_data[user_id]['phone'] = message.contact.phone_number
    bot.send_message(user_id, "✅ Спасибо! Теперь выберите подходящее предложение.")
    send_offer(user_id)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.chat.id
    if user_id in user_data and user_data[user_id]['step'] == 1:
        bot.send_message(user_id, "📞 Пожалуйста, отправьте свой номер телефона как контакт.")
    else:
        send_offer(user_id)

def send_offer(user_id):
    import random
    offer = random.choice(offers)
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🔁 Показать другое предложение", callback_data='next_offer'))
    bot.send_message(user_id, offer, parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'next_offer')
def callback_next_offer(call):
    send_offer(call.message.chat.id)

# Flask webhook
@app.route(f'/{API_TOKEN}', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200

@app.route('/')
def index():
    return "KiCheckBot is alive!", 200
