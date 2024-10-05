from flask import Flask, render_template, send_file, Response

app: Flask = Flask(__name__)

info_url: str = 'https://cloud-api.yandex.net/v1/disk/public/resources'
download_url: str = 'https://cloud-api.yandex.net/v1/disk/public/resources/download'


@app.route('/')
def index() -> str:
    return render_template('index.html')


@app.route('folder')
def folder() -> str:
    return render_template('folder.html')


@app.route('download')
def download() -> Response:
    return send_file()


if __name__ == '__main__':
    app.run(debug=True)
