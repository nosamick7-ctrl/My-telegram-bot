import telebot

API_TOKEN = '8767144395:AAH_x1oO-hjWjzB2SdS_Mxzj0OcSyFa61lc'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "which kain number you fey find!")

@bot.message_handler(commands=['get_number'])
def handle_get_number(message):
    bot.reply_to(message, "baba go work.")

bot.infinity_polling()


