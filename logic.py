# Файл: logic.py

from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_MODEL

# Словарь для хранения активных чатов {chat_id: ChatSession}
active_chats = {}

class GeminiChatbot:
    """Класс для управления сессиями чата с Gemini."""
    
    def __init__(self, api_key: str, model_name: str):
        """Инициализирует клиент Gemini."""
        if not api_key:
            raise ValueError("API Key for Gemini is not set.")
            
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        
    def get_chat_session(self, chat_id: int):
        """
        Возвращает существующую сессию чата или создает новую.
        Используется для сохранения контекста беседы.
        """
        if chat_id not in active_chats:
            # Создаем новую сессию чата
            chat = self.client.chats.create(model=self.model_name)
            active_chats[chat_id] = chat
            print(f"Новая сессия чата создана для ID: {chat_id}")
            
        return active_chats[chat_id]

    def reset_chat_session(self, chat_id: int):
        """Сбрасывает контекст, удаляя чат из словаря."""
        if chat_id in active_chats:
            del active_chats[chat_id]
            return True
        return False

    def generate_response(self, chat_id: int, prompt: str) -> str:
        """
        Отправляет сообщение в Gemini и возвращает ответ.
        """
        try:
            chat = self.get_chat_session(chat_id)
            
            # Отправляем сообщение в чат для сохранения истории
            response = chat.send_message(prompt)
            
            return response.text
            
        except Exception as e:
            print(f"Ошибка при обращении к Gemini API: {e}")
            return "Произошла ошибка при получении ответа от Gemini."

# Создаем единственный экземпляр чат-бота для использования в main.py
gemini_bot = GeminiChatbot(
    api_key=GEMINI_API_KEY, 
    model_name=GEMINI_MODEL
)