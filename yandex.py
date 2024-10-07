from flask import session
import requests

info_url: str = 'https://cloud-api.yandex.net/v1/disk/public/resources'


def get_files_list(public_key, path):
    headers = {
        'Accept': 'application/json',
        'Authorization': f'OAuth {session.get('yandex_token')}'
    }
    params = {
        'public_key': public_key,
        'path': path
    }
    response = requests.get(url=info_url, headers=headers, params=params)
    if response.status_code != 200:
        return []
    files_list = response.json().get('_embedded').get('items')
    return files_list
