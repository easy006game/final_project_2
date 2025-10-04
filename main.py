# Файл: main.py

import telebot
import logging
from telebot.types import Message
from config import TELEGRAM_BOT_TOKEN
from logic import gemini_bot

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализация бота telebot
if not TELEGRAM_BOT_TOKEN:
    logger.error("Токен Telegram-бота не найден. Проверьте файл .env.")
    exit(1)
    
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    """Обрабатывает команду /start."""
    bot.reply_to(
        message, 
        'Привет! Я чат-бот, работающий на Gemini. Просто напишите мне что-нибудь, и я отвечу!'
    )
    logger.info(f"Команда /start получена от {message.chat.id}")


@bot.message_handler(commands=['new_chat'])
def reset_chat(message: Message):
    """Обрабатывает команду /new_chat для сброса контекста."""
    chat_id = message.chat.id
    if gemini_bot.reset_chat_session(chat_id):
        response_text = 'Контекст беседы сброшен. Начнем новый разговор!'
    else:
        response_text = 'Контекст не был активен, но новый разговор готов начаться!'
        
    bot.reply_to(message, response_text)
    logger.info(f"Контекст сброшен для {chat_id}")


@bot.message_handler(content_types=['text'])
def handle_text_message(message: Message):
    """Обрабатывает все текстовые сообщения, отправляя их в Gemini."""
    
    user_message = message.text
    chat_id = message.chat.id
    
    logger.info(f"Получено сообщение от {chat_id}: {user_message}")

    # Уведомляем пользователя, что ответ генерируется (имитация "печатает...")
    bot.send_chat_action(chat_id, 'typing')
    
    # Получаем ответ от Gemini
    gemini_response = gemini_bot.generate_response(chat_id, user_message)
    
    # Отправляем ответ обратно в Telegram
    bot.reply_to(message, gemini_response)


def main():
    """Запуск бота."""
    logger.info("Бот запущен и готов к работе (используется long polling)...")
    # Запускаем постоянный опрос (polling) Telegram API
    bot.infinity_polling()

if __name__ == '__main__':
    main()