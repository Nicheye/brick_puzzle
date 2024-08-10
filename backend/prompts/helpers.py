import requests
import shutil
from prompts.models import Prompt, Style, Color
from django.db.models import Count
from prompts.constances.colors import COLORS
from prompts.constances.styles import STYLES
from authentification.models import User


def get_image(response, user, token, is_common=False):
    if not response or 'choices' not in response or not response['choices']:
        print("Invalid response format")
        return None

    # Navigate to the message content within the choices list
    content = response['choices'][0]['message']['content']
    start = content.find('src=\"') + len('src=\"')
    finish = content.find('\"', start)
    if start == -1 or finish == -1:
        print("Could not find image URL in response content")
        return None

    id = content[start:finish]
    print(f"Image ID: {id}")
    url = f"https://gigachat.devices.sberbank.ru/api/v1/files/{id}/content"
    headers = {
        'Accept': 'application/jpg',
        'Authorization': f'Bearer {token}'
    }
    response = requests.request("GET", url, headers=headers, stream=True, verify=False)
    print(response)
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} when fetching the image")
        return None
    if is_common is False:
        image_path = f'backend/media/media/images/{user}.jpg'
        with open(image_path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)

        print(f"Saved image to {image_path}")
        print(f"user! {user}")
        prompt = Prompt.objects.filter(created_by=User.objects.get(id=int(user)))
        print(prompt.count())
        if prompt.count() > 0:
            prompt = prompt.first()
            prompt.position = Prompt.objects.filter(is_approved=True).count() + 1
            prompt.image = image_path  # Update to store the image path
            prompt.is_approved = True
            prompt.save()

        return f'{user}.jpg'
    else:
        image_path = 'backend/media/media/images/common_pic.jpg'
        with open(image_path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        return f'{image_path}'


def get_most_popular_style():
    most_popular = Style.objects.values('style').annotate(style_count=Count('style')).order_by('-style_count').first()
    if most_popular:
        return dict(STYLES).get(most_popular['style'], "Unknown")
    return None


def get_most_popular_color():
    most_popular = Color.objects.values('color').annotate(style_count=Count('color')).order_by('-color_count').first()
    if most_popular:
        return dict(COLORS).get(most_popular['color'], "Unknown")
    return None
