# Файл: main.py

import telebot
import logging
import sys
from telebot.types import Message

# Импорт конфигурации и логики
from config import TELEGRAM_BOT_TOKEN
from logic import gemini_bot
from logger import log_message 

# --- НАСТРОЙКА ЛОГИРОВАНИЯ ---
# Настройка логирования для вывода в консоль
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__) 
# -----------------------------

# Инициализация бота telebot
if not TELEGRAM_BOT_TOKEN:
    logger.error("🚫 Токен Telegram-бота не найден в config.py. Проверьте файл .env.")
    # Прекращаем выполнение, если токен не найден
    sys.exit(1)
    
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    """Обрабатывает команду /start."""
    bot.reply_to(
        message, 
        '🤖 Привет! Я чат-бот, работающий на Gemini. Просто напишите мне что-нибудь, и я отвечу!'
    )
    # Логируем команду
    log_message(message.chat.id, 'SYSTEM', f"Command /start")
    logger.info(f"Команда /start получена от {message.chat.id}")


@bot.message_handler(commands=['new_chat'])
def reset_chat(message: Message):
    """Обрабатывает команду /new_chat для сброса контекста."""
    chat_id = message.chat.id
    if gemini_bot.reset_chat_session(chat_id):
        response_text = '✨ Контекст беседы сброшен. Начнем новый разговор!'
    else:
        response_text = '💫 Контекст не был активен, но новый разговор готов начаться!'
        
    bot.reply_to(message, response_text)
    # Логируем команду сброса
    log_message(chat_id, 'SYSTEM', f"Command /new_chat executed. Context reset.")
    logger.info(f"Контекст сброшен для {chat_id}")


@bot.message_handler(content_types=['text'])
def handle_text_message(message: Message):
    """Обрабатывает все текстовые сообщения, отправляя их в Gemini."""
    
    user_message = message.text
    chat_id = message.chat.id
    
    logger.info(f"Получено сообщение от {chat_id}: {user_message}")
    
    # 1. Логируем сообщение пользователя
    log_message(chat_id, 'USER', user_message) 

    # Показываем статус "печатает..."
    bot.send_chat_action(chat_id, 'typing')
    
    # Получаем ответ от Gemini
    gemini_response = gemini_bot.generate_response(chat_id, user_message)
    
    # 2. Логируем ответ Gemini
    log_message(chat_id, 'GEMINI', gemini_response) 
    
    # Отправляем ответ обратно в Telegram
    bot.reply_to(message, gemini_response)


def main():
    """Запуск бота."""
    logger.info("✅ Бот запущен и готов к работе (используется long polling)...")
    # Запускаем постоянный опрос (polling) Telegram API
    bot.infinity_polling()

if __name__ == '__main__':
    # Если запуск не удастся из-за ошибки в logic.py (например, отсутствия GEMINI_API_KEY),
    # то main не будет вызвана, а ошибка будет выведена.
    # Если же ошибки нет, то запускаем:
    main()