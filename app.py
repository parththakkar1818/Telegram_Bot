import os
import telebot
import requests
from dotenv import load_dotenv
from telebot.types import ReplyKeyboardRemove

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

selected_sign = ""

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

def get_daily_horoscope(sign: str, day: str) -> dict:
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url, params)
    response.raise_for_status()  # Raise exception for non-200 status codes
    return response.json()

def day_handler(message):
    global selected_sign
    sign = message.text
    if sign.lower() == "cancel":
        bot.send_message(message.chat.id, "Operation canceled.")
    else:
        selected_sign = sign.capitalize()
        text = "What day do you want to know?\nChoose one: *TODAY*, *TOMORROW*, *YESTERDAY*, or a date in format YYYY-MM-DD."
        sent_msg = bot.send_message(
            message.chat.id, text, reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")
        bot.register_next_step_handler(sent_msg, fetch_horoscope)

def fetch_horoscope(message):
    global selected_sign
    if not selected_sign:
        bot.send_message(message.chat.id, "Please select a zodiac sign first.")
        return
    day = message.text
    try:
        horoscope = get_daily_horoscope(selected_sign, day)
        data = horoscope["data"]
        horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Sign:* {selected_sign}\n*Day:* {data["date"]}'
        bot.send_message(message.chat.id, "Here's your horoscope!")
        bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")
    except KeyError:
        bot.send_message(message.chat.id, "Invalid response from API. Please try again later.")
    except requests.exceptions.HTTPError as e:
        bot.send_message(message.chat.id, "Enter Valid Input...")
    except Exception as e:
        bot.send_message(message.chat.id, f"An unexpected error occurred: {e}")
    finally:
        # Reset selected_sign after processing
        selected_sign = ""

@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    global selected_sign
    text = "What's your zodiac sign?"
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=4)
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    keyboard.add(*signs)
    keyboard.add("Cancel")
    sent_msg = bot.send_message(
        message.chat.id, text, reply_markup=keyboard, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, day_handler)

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()
