from flask import request, session
import requests

info_url: str = 'https://cloud-api.yandex.net/v1/disk/public/resources'
download_url: str = 'https://cloud-api.yandex.net/v1/disk/public/resources/download'


def get_files_list(public_key: str, path: str) -> list:
    headers: dict = {
        'Accept': 'application/json',
        'Authorization': f'OAuth {session.get('yandex_token')}'
    }
    params: dict = {
        'public_key': public_key,
        'path': path
    }
    response: requests.Response = requests.get(
        url=info_url, headers=headers, params=params)
    if response.status_code != 200:
        return []
    files_list: list = response.json().get('_embedded').get('items')
    return files_list


def get_download_link(path: str) -> list:
    public_key: str = request.form.get('public_key')
    response: requests.Response = requests.get(url=download_url, params={
        'public_key': public_key,
        'path': path
    })
    if response.status_code != 200:
        return ''
    return response.json()['href']


def get_download_links(paths: str) -> list:
    file_urls: list = []

    for path in paths:
        link: str = get_download_link(path)
        if not link:
            return []
        file_urls.append(link)
    return file_urls
