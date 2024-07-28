import requests
import shutil


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

    with open(f'{user}.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    return f'{user}.jpg'