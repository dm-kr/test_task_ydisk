from flask import Flask, Response, redirect, render_template, send_file, url_for, session
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os

from decorators import need_login

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

info_url: str = 'https://cloud-api.yandex.net/v1/disk/public/resources'
download_url: str = 'https://cloud-api.yandex.net/v1/disk/public/resources/download'


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
    return render_template('folder.html')


@app.route('/download')
@need_login
def download() -> Response:
    return send_file()


if __name__ == '__main__':
    app.run(debug=True)
