from prompts.celery import app
import requests
from prompts.helpers import get_image
from prompts.models import Prompt
from prompts.helpers import get_most_popular_color, get_most_popular_style
from dotenv import load_dotenv
from prompts.scripts import grid_image, summarize_text
import warnings
load_dotenv()


def get_access_token():
    warnings.filterwarnings('ignore', message='Unverified HTTPS request')

    oauth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    oauth_payload = {'scope': 'GIGACHAT_API_PERS'}
    oauth_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': 'eb1c7911-998f-4720-91d8-e5177c943f5d',
        'Authorization': 'Basic ZWIxYzc5MTEtOTk4Zi00NzIwLTkxZDgtZTUxNzdjOTQzZjVkOmEyYzI5MzZkLTVkMjgtNDI0ZC1iMWE2LTJiMTRjOTk4YjA1Nw=='
    }

    oauth_response = requests.post(oauth_url, headers=oauth_headers, data=oauth_payload, verify=False)
    oauth_response.raise_for_status()

    access_token = oauth_response.json().get('access_token')

    if not access_token:
        raise ValueError('Access token not found in the response')

    return access_token

@app.task
def generate_image(prompt, style, color, user, is_common=False):
    api_key = get_access_token()

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

        response = requests.post(url, headers=headers, json=data, verify=False)
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            print(response.text)
            return None
        print(response.json())
        image = get_image(response.json(), user, api_key, is_common)
        return image

    except Exception as e:
        print(str(e))
        return None


@app.task
def regenerate_grid():
    if Prompt.objects.filter(is_approved=True).count() % 5 != 0:
        pass
    grid_image.save('media/images/grid.jpg')


@app.task
def generate_common_image():
    all_text = ''
    for prompt in Prompt.objects.all():
        all_text += prompt.prompt
    summary = summarize_text(all_text)
    color = get_most_popular_color()
    style = get_most_popular_style()
    generate_image(summary, style, color, 1, True)
