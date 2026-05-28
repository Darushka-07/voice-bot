import os
import subprocess
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    # Перевіряємо де знаходиться ffmpeg
    which = subprocess.run(["which", "ffmpeg"], capture_output=True, text=True).stdout.strip()
    find = subprocess.run(["find", "/", "-name", "ffmpeg", "-type", "f"], capture_output=True, text=True).stdout.strip()
    path = os.environ.get("PATH", "")
    
    bot.reply_to(message, f"which: {which}\nfind: {find}\nPATH: {path}")

bot.polling()
