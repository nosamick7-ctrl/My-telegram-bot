import telebot

API_TOKEN = '8767144395:AAFL9bmS1ETEd0bpPItx0_kQv4_8CE_0s9Q'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome!")

@bot.message_handler(commands=['get_number'])
def handle_get_number(message):
    bot.reply_to(message, "Your number is ready.")

bot.infinity_polling()
