# logic.py
from openai import OpenAI
import config

# Создаём клиента OpenAI
client = OpenAI(api_key=config.OPENAI_API_KEY)

def ask_gpt(prompt: str) -> str:
    """
    Отправка текста в GPT и возврат ответа
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # можно заменить на gpt-4o или gpt-3.5-turbo
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка при запросе к GPT: {e}"
