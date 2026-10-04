import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from telebot import types
import random


# =========================
# RENDER DUMMY HTTP SERVER
# =========================

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is live!")

    def log_message(self, format, *args):
        # Suppress standard HTTP request logging in the terminal
        return


def run_http_server():
    # Render automatically sets the PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"HTTP dummy server listening on port {port}...")
    httpd.serve_forever()


# =========================
# CONFIGURATION
# =========================

API_TOKEN = os.getenv("BOT_TOKEN")

if not API_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is not set. Add your Telegram bot token "
        "as an environment variable named BOT_TOKEN."
    )

bot = telebot.TeleBot(API_TOKEN)
Pakistan = [
    "923322314135",
    "923325533793",
    "923315533299",
    "923335575165",
    "923327438814",
    "923367734258",
    "923375051100",
    "923343609380",
    "923315130848",
    "923315535413",
    "923322315070",
    "923315533208",
    "923367733252",
    "923343604224",
    "923315132393",
    "923315131381",
    "923368119647",
    "923335574259",
    "923315535917",
    "923375050142",
    "923343603327",
    "923325531472",
    "923368117377",
    "923368116294",
    "923327435187",
    "923315535661",
    "923343601121",
    "923327435845",
    "923367734424",
    "923366740271",
    "923367730363",
    "923315135347",
    "923327433667",
    "923315533004",
    "923375059105",
    "923368117865",
    "923343602082",
    "923322315688",
    "923327437754",
    "923343604832",
    "923361111335",
    "923315534727",
    "923366747969",
    "923335575323",
    "923368116553",
    "923327435424",
    "923343601411",
    "923366744327"
]

# =========================
# KEYBOARDS
# =========================

def main_menu_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)

    markup.add(
        types.InlineKeyboardButton(
            "📱 Get Number",
            callback_data="get_number"
        )
    )

    markup.add(
        types.InlineKeyboardButton(
            "💰 Balance",
            callback_data="balance"
        )
    )

    markup.add(
        types.InlineKeyboardButton(
            "👥 Refer Friends",
            callback_data="refer"
        )
    )

    return markup


    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "🔄 Refresh Number",
            callback_data="refresh_number"
        ),
        types.InlineKeyboardButton(
            "⬅️ Back",
            callback_data="main_menu"
        )
    )
    return markup


# =========================
# START COMMAND
# =========================

@bot.message_handler(commands=["start"])
def send_welcome(message):
    welcome_text = (
        f"Welcome, {message.from_user.first_name}! 👋\n\n"
        "What can I help you with?"
    )

    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=main_menu_markup()
    )


# =========================
# GET NUMBER COMMAND
# =========================

@bot.message_handler(commands=["get_number"])
def handle_get_number(message):
    bot.send_message(
        message.chat.id,
        "📱 Your virtual number:\n\n"
        "No number is currently available.",
        reply_markup=back_markup()
    )


# =========================
# CALLBACK HANDLER
# =========================

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    # Stop Telegram's loading animation
    bot.answer_callback_query(call.id)

    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == "get_number":
        chosen_number = random.choice(Pakistan)
        text = (
            "📱 Get Number\n\n"
            f"Your virtual number:\n{chosen_number}"
       )
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=back_markup()
        )

    elif call.data == "balance":

        text = (
            "💰 Your Balance\n\n"
            "$0.0000"
        )

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=back_markup()
        )

    elif call.data == "refer":

        # Creates the user's actual Telegram referral link
        bot_username = bot.get_me().username

        referral_link = (
            f"https://t.me/{bot_username}?start={call.from_user.id}"
        )

        text = (
            "👥 Refer Friends\n\n"
            "Invite your friends using your personal referral link:\n\n"
            f"{referral_link}"
        )

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=back_markup()
        )

    elif call.data == "main_menu":

        text = (
            f"Welcome, {call.from_user.first_name}! 👋\n\n"
            "What can I help you with?"
        )

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=main_menu_markup()
        )


# =========================
# ERROR HANDLING
# =========================

@bot.message_handler(func=lambda message: True)
def unknown_message(message):
    bot.send_message(
        message.chat.id,
        "Please use the buttons below 👇",
        reply_markup=main_menu_markup()
    )


# =========================
# START BOT
# =========================

if __name__ == "__main__":
    # Start the dummy HTTP server in a separate background thread
    server_thread = threading.Thread(target=run_http_server, daemon=True)
    server_thread.start()

    print("Bot is running...")

    bot.infinity_polling(
        skip_pending=True,
        allowed_updates=["message", "callback_query"]
    )
