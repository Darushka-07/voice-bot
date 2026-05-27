import os
import requests
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

def transcribe_audio(file_path):
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    with open(file_path, "rb") as f:
        data = f.read()
    
    response = requests.post(API_URL, headers=headers, data=data)
    result = response.json()
    return result.get("text", "Не вдалося розпізнати")

@bot.message_handler(content_types=["voice"])
def handle_voice(message):
    bot.reply_to(message, "⏳ Транскрибую...")
    
    # Завантажуємо файл
    file_info = bot.get_file(message.voice.file_id)
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"
    
    audio_data = requests.get(file_url).content
    with open("voice.ogg", "wb") as f:
        f.write(audio_data)
    
    # Транскрибуємо
    text = transcribe_audio("voice.ogg")
    bot.reply_to(message, f"📝 {text}")

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Привіт! 👋 Надішли мені голосове повідомлення — я перетворю його на текст.")

bot.polling()
