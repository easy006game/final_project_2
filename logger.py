# Файл: logger.py

from datetime import datetime
import os

# Имя файла, в который будут записываться логи
LOG_FILE_NAME = "chat_log.txt"

def log_message(chat_id: int, sender: str, text: str):
    """
    Записывает сообщение в файл chat_log.txt с отметкой времени.

    :param chat_id: ID чата Telegram.
    :param sender: Отправитель сообщения ('USER' или 'GEMINI').
    :param text: Текст сообщения.
    """
    
    # Форматируем текущее время
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    
    # Форматируем строку лога
    log_entry = f"{timestamp} [CHAT:{chat_id}] [{sender}]: {text}\n"
    
    try:
        # Открываем файл в режиме добавления ('a') и записываем
        with open(LOG_FILE_NAME, 'a', encoding='utf-8') as f:
            f.write(log_entry)
            
    except Exception as e:
        # Если произошла ошибка записи (например, нет прав)
        print(f"ОШИБКА ЛОГИРОВАНИЯ: Не удалось записать в файл {LOG_FILE_NAME}. {e}")

# При запуске создадим пустой файл или добавим разделитель
if not os.path.exists(LOG_FILE_NAME):
    with open(LOG_FILE_NAME, 'w', encoding='utf-8') as f:
        f.write("--- НАЧАЛО ЛОГА ЧАТ-БОТА GEMINI ---\n")
else:
    with open(LOG_FILE_NAME, 'a', encoding='utf-8') as f:
        f.write("\n--- СЕССИЯ ВОЗОБНОВЛЕНА ---\n")