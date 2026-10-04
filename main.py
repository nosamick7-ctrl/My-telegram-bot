import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from telebot import types


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


def back_markup():
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(
            "⬅️️ Back",
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

        text = (
            "📱 Get Number\n\n"
            "No virtual number is currently available."
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
