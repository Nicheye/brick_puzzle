from prompts.celery import app
import requests
from prompts.helpers import get_image
from dotenv import load_dotenv
import os

load_dotenv()


@app.task
def generate_image(prompt, style, color, user):
    api_key = os.getenv('SBER_KEY')
    try:
        url = 'https://gigachat.devices.sberbank.ru/api/v1/chat/completions'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        data = {
            "model": "GigaChat",
            "messages": [
                {
                    "role": "system",
                    "content": "Ты — Василий Кандинский"
                },
                {
                    "role": "user",
                    "content": f"Нарисуй {prompt} {color} цвета в стиле {style}"
                }
            ],
            "function_call": "auto"
        }

        response = requests.post(url, headers=headers, json=data)
        image = get_image(response.json(), user, api_key)
        return image
    except Exception as e:
        return str(e)
    
