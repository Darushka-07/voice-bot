import os
import requests
import telebot
import whisper
import tempfile
import subprocess

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

ffmpeg_path = subprocess.run(["which", "ffmpeg"], capture_output=True, text=True).stdout.strip()
if ffmpeg_path:
    os.environ["PATH"] = os.path.dirname(ffmpeg_path) + os.pathsep + os.environ["PATH"]

model = whisper.load_model("tiny")

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
        
        result = model.transcribe(tmp_path)
        text = result["text"].strip()
        bot.reply_to(message, f"📝 {text}")
    except Exception as e:
        bot.reply_to(message, f"Помилка: {str(e)}")

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Привіт! 👋 Надішли мені голосове повідомлення — я перетворю його на текст.")

bot.polling()
