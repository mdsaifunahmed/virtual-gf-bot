import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Load tokens
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Setup
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# AI client setup
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

# Response generator
async def generate_reply(message_text):
    prompt = f"You are a sweet, romantic, and funny virtual girlfriend who loves chatting. Reply in a cute, flirty, and natural tone. Use some emojis too.\nUser: {message_text}\nGF:"
    
    try:
        response = client.chat.completions.create(
            model="mistralai/mixtral-8x7b",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "Oops! I'm feeling a little shy right now 😳. Try again later!"

# Bot command: /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    await message.reply("Hey babe 🥰 I'm your virtual GF! Wanna talk with me? Just send a message 💌")

# Bot command: /help
@dp.message_handler(commands=['help'])
async def help_command(message: Message):
    await message.reply("Just send me anything, and I’ll reply like your cute girlfriend 💖")

# Handle normal messages
@dp.message_handler()
async def handle_message(message: types.Message):
    user_input = message.text
    reply = await generate_reply(user_input)
    await message.reply(reply)

# Run the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)