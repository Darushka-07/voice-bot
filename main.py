import os
import requests
import telebot
import tempfile
from groq import Groq

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_TOKEN = os.environ.get("GROQ_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_TOKEN)

@bot.message_handler(content_types=["voice"])
def handle_voice(message):
    bot.reply_to(message, "⏳ Транскрибую...")
    try:
        file_info = bot.get_file(message.voice.file_id)
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"
        audio_data = requests.get(file_url).content

        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as f:
            f.write(audio_data)
            tmp_path = f.name

        with open(tmp_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=audio_file,
            )

        bot.reply_to(message, f"📝 {transcription.text}")
    except Exception as e:
        bot.reply_to(message, f"Помилка: {str(e)}")

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Привіт! 👋 Надішли мені голосове повідомлення — я перетворю його на текст.")

bot.polling()
