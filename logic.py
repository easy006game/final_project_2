# logic.py
import google.generativeai as genai
import config

# Настраиваем API-ключ
genai.configure(api_key=config.GEMINI_API_KEY)

def ask_gpt(prompt: str) -> str:
    """
    Отправляет сообщение в Google Gemini и возвращает ответ
    """
    try:
        # Используем модель Gemini 1.5 Flash (очень быстрая и бесплатная)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        return response.text if response.text else "❌ Gemini не вернул ответ."

    except Exception as e:
        return f"Ошибка при обращении к Gemini API: {e}"
