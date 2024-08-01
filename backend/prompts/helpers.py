import requests
import shutil
from prompts.models import Prompt
from prompts.scripts import grid_image

def get_image(response, user, token):
    content = str(response['message']['content'])
    start = content.find('src=\"') + len('src=\"')
    finish = content.find('\"', start)
    id = content[start:finish]
    url = f"https://gigachat.devices.sberbank.ru/api/v1/files/{id}/content"
    headers = {
        'Accept': 'application/jpg',
        'Authorization': f'Bearer {token}'
    }
    response = requests.request("GET", url, headers=headers, stream=True)

    with open(f'media/images/{user}.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

    del response
    prompt = Prompt.objects.filter(created_by__username=user)
    if prompt.count() > 0:
        prompt = prompt.first()
        prompt.image = out_file
        prompt.save()
        
    return f'{user}.jpg'