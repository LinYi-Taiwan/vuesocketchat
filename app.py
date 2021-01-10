from flask import Flask, render_template, make_response, redirect
from flask_socketio import SocketIO, send, emit
import json
import os

app = Flask(__name__)
socketio = SocketIO(app)

USERS=set()

@app.route('/')
def index():
    print('index')
    return render_template('index.html')


@socketio.on("message")
def handleMessage(message):
    data = json.loads(message)
    print(data)
    message = ''
    if data['type']=='login':
        USERS.add(data['content'])
        if len(USERS)!=0:
            message = json.dumps(
                    {"type": "login", "content": data["content"], "user_list":list(USERS)})

    elif data['type']=='send':
        message = json.dumps(
                    {"type": "user", "content": data["content"], "from": data['name']})
    elif data["type"] == 'logout':
            print(data['content'])

            USERS.remove(data["content"])
            if len(USERS) != 0:  # asyncio.wait doesn't accept an empty list
                message = json.dumps(
                    {"type": "logout", "content": data["content"], "user_list": list(USERS)})
    emit("new_message", message, broadcast=True)


if __name__ == "__main__":
    print('name')
    socketio.run(app, debug=True, host='0.0.0.0', port=1234)
