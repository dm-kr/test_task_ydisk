from flask import Flask, render_template, send_file

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('folder')
def folder():
    return render_template('folder.html')


@app.route('download')
def download():
    return send_file()


if __name__ == '__main__':
    app.run(debug=True)
