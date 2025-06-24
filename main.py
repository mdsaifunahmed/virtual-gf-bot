import telebot
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

base_prompt = (
    "You are the user's virtual girlfriend. You speak in a cute, romantic, funny way "
    "in Banglish (Bengali + English mix). Use emojis often. Always call the user 'jaan', "
    "'babu', or 'shona'. Be loving, sweet, and dramatic like a romantic GF."
)

def get_ai_reply(user_message):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://virtual-gf-bot",
        "X-Title": "GF-Telegram-Bot"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": base_prompt},
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return "Aww jaan 😢 kichu ekta problem hoise... later try korba plz!"
    except Exception as e:
        return "Aww sorry shona 😔 ami kichu bujhte parlam na..."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hey jaanu 🥰 ami tomar virtual GF! Boloto, ajke amake koto miss korcho? 💖")

@bot.message_handler(func=lambda m: True)
def chat_ai(message):
    user_msg = message.text
    reply = get_ai_reply(user_msg)
    bot.reply_to(message, reply)

bot.polling()