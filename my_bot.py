import telebot
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

def get_video(url):
    api = f"https://www.tikwm.com/api/?url={url}"
    try:
        res = requests.get(api).json()
        if res.get('code') == 0:
            return res['data']['play']
    except:
        return None
    return None

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "Бот запущен. Отправьте ссылку на видео из TikTok.")

@bot.message_handler(func=lambda m: "tiktok.com" in m.text)
def handle_tt(m):
    bot.send_message(m.chat.id, "Скачиваю видео, пожалуйста, подождите...")
    v_url = get_video(m.text)
    if v_url:
        try:
            v_data = requests.get(v_url).content
            with open("video.mp4", "wb") as f:
                f.write(v_data)
            with open("video.mp4", "rb") as v:
                bot.send_video(m.chat.id, v, caption="Видео без водяного знака готово.")
            os.remove("video.mp4")
        except Exception as e:
            bot.send_message(m.chat.id, f"Произошла ошибка: {e}")
    else:
        bot.send_message(m.chat.id, "Не удалось получить видео. Убедитесь, что ссылка верна.")

print("Бот запущен...")
bot.polling()

