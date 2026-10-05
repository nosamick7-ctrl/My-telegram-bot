import os
import threading
import random
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
        return


def run_http_server():
    port = int(os.environ.get("PORT", 8080))
    server_address = ("0.0.0.0", port)

    httpd = HTTPServer(
        server_address,
        SimpleHTTPRequestHandler
    )

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
# TEST NUMBERS
# =========================

Nigeria🇳🇬 = [
    "2348022215551",
    "2348022254679",
    "2348022612707",
    "2348022669464",
    "2348022639587",
    "2348022604466",
    "2348022256419",
    "2348022278649",
    "2348022240161",
    "2348022680037",
    "2348022202933",
    "2348022203529",
    "2348022228385",
    "2348022689424",
    "2348022685837",
    "2348022211667",
    "2348022640543",
    "2348022647994",
    "2348022290310",
    "2348022662836",
    "2348022283892",
    "2348022288007",
    "2348022601057",
    "2348022658518",
    "2348022639929",
    "2348022298749",
    "2348022662041",
    "2348022670268",
    "2348022616319",
    "2348022263861",
    "2348022626641",
    "2348022663863",
    "2348022606064",
    "2348022290366",
    "2348022290785",
    "2348022216644",
    "2348022298794",
    "2348022253680",
    "2348022204225",
    "2348022239403",
    "2348022285682",
    "2348022238009",
    "2348022275800",
    "2348022674154",
    "2348022613717",
    "2348022236746",
    "2348022267616",
    "2348022613470",
    "2348022682480",
    "2348022291006",
    "2348022680603",
    "2348022261455",
    "2348022285369",
    "2348022668982",
    "2348022668680",
    "2348022666038",
    "2348022696707",
    "2348022220527",
    "2348022205049",
    "2348022690795",
    "2348022200550",
    "2348022281933",
    "2348022634877",
    "2348022670711",
    "2348022663123",
    "2348022656607",
    "2348022233928",
    "2348022602189",
    "2348022624512",
    "2348022226267",
    "2348022268062",
    "2348022271521",
    "2348022204549",
    "2348022686097",
    "2348022240399",
    "2348022656498",
    "2348022262390",
    "2348022220812",
    "2348022694297",
    "2348022633850",
    "2348022687892",
    "2348022644424",
    "2348022215634",
    "2348022646303",
    "2348022605910",
    "2348022690587",
    "2348022268801",
    "2348022642568",
    "2348022210054",
    "2348022645410",
    "2348022603668",
    "2348022237832",
    "2348022247286",
    "2348022646741",
    "2348022208772",
    "2348022619678",
    "2348022698397",
    "2348022676472",
    "2348022290774",
    "2348022206411",
    "2348022295145",
    "2348022258783",
    "2348022297669",
    "2348022684589",
    "2348022267702",
    "2348022246685",
    "2348022672753",
    "2348022255341",
    "2348022652379",
    "2348022633789",
    "2348022266991"
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
        ),
        types.InlineKeyboardButton(
            "💰 Balance",
            callback_data="balance"
        ),
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
    chosen_number = random.choice(Nigeria🇳🇬)

    bot.send_message(
        message.chat.id,
        "📱 Your test number:\n\n"
        f"{chosen_number}",
        reply_markup=back_markup()
    )


# =========================
# CALLBACK HANDLER
# =========================

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    bot.answer_callback_query(call.id)

    chat_id = call.message.chat.id
    message_id = call.message.message_id

    try:
        # -------------------------
        # GET NUMBER
        # -------------------------
        if call.data == "get_number":
            chosen_number = random.choice(Nigeria)
            text = (
                "📱 Get Number\n\n"
                f"Your test number:\n{chosen_number}"
            )
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=back_markup()
            )

        # -------------------------
        # REFRESH NUMBER
        # -------------------------
        elif call.data == "refresh_number":
            chosen_number = random.choice(Nigeria)
            text = (
                "📱 Get Number\n\n"
                f"Your new test number:\n{chosen_number}"
            )
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=back_markup()
            )

        # -------------------------
        # BALANCE
        # -------------------------
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

        # -------------------------
        # REFER
        # -------------------------
        elif call.data == "refer":
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

        # -------------------------
        # BACK TO MAIN MENU
        # -------------------------
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
    except telebot.apihelper.ApiTelegramException as e:
        if "message is not modified" not in str(e):
            raise e


# =========================
# UNKNOWN MESSAGE
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
    server_thread = threading.Thread(
        target=run_http_server,
        daemon=True
    )
    server_thread.start()

    print("Bot is running...")

    bot.infinity_polling(
        skip_pending=True,
        allowed_updates=[
            "message",
            "callback_query"
        ]
    )
