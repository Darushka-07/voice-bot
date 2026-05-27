import os
import requests
import telebot
import subprocess

BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

def transcribe_audio(file_path):
    try:
        result = subprocess.run(
            ["whisper", file_path, "--model", "tiny", "--output_format", "txt", "--output_dir", "/tmp"],
            capture_output=True, text=True, timeout=120
        )
        txt_file = "/tmp/" + os.path.basename(file_path).replace(".ogg", ".txt")
        if os.path.exists(txt_file):
            with open(txt_file, "r") as f:
                return f.read().strip()
        return "Не вдалося розпізнати"
    except Exception as e:
        return f"Помилка: {str(e)}"

@bot.message_handler(content_types=["voice"])
def handle_voice(message):
    bot.reply_to(message, "⏳ Транскрибую...")
    file_info = bot.get_file(message.voice.file_id)
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"
    audio_data = requests.get(file_url).content
    with open("/tmp/voice.ogg", "wb") as f:
        f.write(audio_data)
    text = transcribe_audio("/tmp/voice.ogg")
    bot.reply_to(message, f"📝 {text}")

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Привіт! 👋 Надішли мені голосове повідомлення — я перетворю його на текст.")

bot.polling()
