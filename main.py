# main.py
import telebot
import config
from logic import ask_gpt

# Создаём бота
bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

# Обработка сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text

    # Отправляем запрос в GPT
    reply = ask_gpt(user_text)

    # Отправляем ответ пользователю
    bot.reply_to(message, reply)

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
