from flask import Flask

app = Flask(__name__,template_folder='templates')

from app import routes

if __name__ == '__main__':
    app.run(debug=True,port=3000)