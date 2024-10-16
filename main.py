from waitress import serve
from whitenoise import WhiteNoise

from app.server import Application


if __name__ == '__main__':
    app = WhiteNoise(Application(), f'resources/static/')
    serve(app, host='0.0.0.0', port=8080)
