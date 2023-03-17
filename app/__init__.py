from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__,template_folder='templates')

from app import routes


if __name__ == '__main__':
    SocketIO.run(app)