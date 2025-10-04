# main.py
import telebot
import config
from logic import ask_gpt

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    bot.reply_to(message, "⏳ Думаю над ответом...")

    reply = ask_gpt(user_text)
    bot.send_message(message.chat.id, reply)

if __name__ == "__main__":
    print("Бот запущен... (Gemini)")
    bot.infinity_polling()
