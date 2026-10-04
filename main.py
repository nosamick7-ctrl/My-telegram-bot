import telebot
from telebot import types

def main_menu_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Get Number", callback_data="get_number"))
    markup.add(types.InlineKeyboardButton("💰 Balance", callback_data="balance"))
    markup.add(types.InlineKeyboardButton("Refer Friends", callback_data="refer"))
    return markup

def back_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="main_menu"))
    return markup

API_TOKEN = '8767144395:AAH_x1oO-hjWjzB2SdS_Mxzj0OcSyFa61lc'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "welcome baby what can i help you with!")

@bot.message_handler(commands=['get_number'])
def handle_get_number(message):
    bot.reply_to(message, "baba go work.")
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "get_number":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Your virtual number: 080123456789", reply_markup=back_markup())
    elif call.data == "balance":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="💰 Your Balance: $0.0000", reply_markup=back_markup())
    elif call.data == "refer":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Your referral link: https://t.me/bot?start=123", reply_markup=back_markup())
    elif call.data == "main_menu":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Welcome, baby! What can I help you with?", reply_markup=main_menu_markup())

bot.infinity_polling()


