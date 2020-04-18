import os

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

class Channel:
    def __init__(self, creator, name):
        self.creator = creator
        self.name = name
        self.messages = {}
    

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

users = []
channels = []
channel_messeges = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    if username not in users:
        users.append(username)

    return jsonify({'username': username, 'users': users})

@app.route('/main')
def main():
    return render_template("main.html")
    


if __name__ == "__main__":
    socketio.run(app)
