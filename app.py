from flask import Flask, Response, redirect, render_template, send_file, url_for, request, session
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from io import BytesIO
import os
import requests
import zipfile

from decorators import need_login
from yandex import get_files_list, get_download_links

load_dotenv()

app: Flask = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')

oauth: OAuth = OAuth(app)

oauth.register(
    name='yandex',
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    authorize_url='https://oauth.yandex.ru/authorize',
    access_token_url='https://oauth.yandex.ru/token',
    userinfo_endpoint='https://login.yandex.ru/info',
    client_kwargs={'scope': 'login:email login:info'},
)


@app.route('/')
@need_login
def index() -> str:
    return render_template('index.html')


@app.route('/login')
def login() -> None:
    redirect_uri: str = url_for('authorize', _external=True)
    return oauth.yandex.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize() -> Response:
    token: str = oauth.yandex.authorize_access_token()
    session['yandex_token'] = token
    user_info: dict = oauth.yandex.get('https://login.yandex.ru/info').json()
    session['user_info'] = user_info
    return redirect(url_for('index'))


@app.route('/logout')
def logout() -> Response:
    session.pop('yandex_token', None)
    session.pop('user_info', None)
    return redirect(url_for('index'))


@app.route('/folder')
@need_login
def folder() -> str:
    public_key: str = request.args.get('public_key')
    if not public_key:
        return "Публичная ссылка не указана", 400
    path: str = request.args.get('path')
    files_list: list = get_files_list(public_key, path)
    if not files_list:
        return "Ошибка при получении списка файлов", 500
    filetypes: list = [
        {'id': 'all', 'name': 'Все файлы'},
        {'id': 'dir', 'name': 'Папки'},
        {'id': 'document', 'name': 'Документы'},
        {'id': 'image', 'name': 'Картинки'},
    ]
    filetype: str = request.args.get('filetype')
    if filetype and filetype != 'all':
        files_list = list(filter(
            lambda file: file.get('media_type', 'dir') == filetype, files_list))
    current_path: str = request.args.get('path', '').split('/')
    previous_folder: str = f'/{'/'.join(current_path[1:-1])}'
    context: dict = {
        'files': files_list,
        'public_key': public_key,
        'back_link_path': previous_folder if any(current_path) else None,
        'filetypes': filetypes,
        'selected_filetype': filetype,
    }
    return render_template('folder.html', **context)


@app.route('/download')
@need_login
def download() -> Response:
    paths: list = request.form.getlist('selected_files')
    if len(paths) < 1:
        return "Выберите хотя бы один файл", 400
    file_urls: list = get_download_links(paths)
    if not file_urls:
        return "Ошибка при получении загрузочной ссылки", 500
    if len(file_urls) == 1:
        buffer: BytesIO = BytesIO(requests.get(file_urls[0]).content)
        return send_file(buffer, as_attachment=True, download_name=paths[0].split('/')[-1])

    zip_buffer: BytesIO = BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for i in range(len(file_urls)):
            response: requests.Response = requests.get(file_urls[i])
            if response.status_code == 200:
                file_name: str = paths[i].split('/')[-1]
                zip_file.writestr(file_name, response.content)
            else:
                return f"Ошибка при скачивании файла: {file_urls[i]}", 500

    zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        as_attachment=True,
        download_name='files.zip',
        mimetype='application/zip'
    )


if __name__ == '__main__':
    app.run(debug=True)
