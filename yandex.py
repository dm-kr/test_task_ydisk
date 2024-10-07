from flask import request, session
from typing import Dict, List, Any
import requests

from decorators import cache

info_url: str = 'https://cloud-api.yandex.net/v1/disk/public/resources'
download_url: str = 'https://cloud-api.yandex.net/v1/disk/public/resources/download'


@cache(time=30)
def get_files_list(public_key: str, path: str) -> List[Dict[str, Any]]:
    headers: Dict[str, str] = {
        'Accept': 'application/json',
        'Authorization': f'OAuth {session.get('yandex_token')}'
    }
    params: Dict[str, str] = {
        'public_key': public_key,
        'path': path
    }
    response: requests.Response = requests.get(
        url=info_url, headers=headers, params=params)
    if response.status_code != 200:
        return []
    files_list: List[Dict[str, Any]] = response.json().get(
        '_embedded').get('items')
    if not files_list:
        files_list = [{'type': 'nofile'}]
    return files_list


@cache(time=30)
def get_download_link(path: str) -> str:
    public_key: str = request.form.get('public_key')
    response: requests.Response = requests.get(url=download_url, params={
        'public_key': public_key,
        'path': path
    })
    if response.status_code != 200:
        return ''
    return response.json()['href']


def get_download_links(paths: str) -> List[str]:
    file_urls: List[str] = []

    for path in paths:
        link: str = get_download_link(path)
        if not link:
            return []
        file_urls.append(link)
    return file_urls
