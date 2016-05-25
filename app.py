import socketio
import eventlet

from flask import Flask, request

sio = socketio.Server()
# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

@app.route('/', methods=['GET'])
def root():
    return app.send_static_file('index.html')

@sio.on('connect', namespace='/chat')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('chat message', namespace='/chat')
def message(sid, data):
    print("message ", data)
    sio.emit(sid, 'reply')

@sio.on('disconnect', namespace='/chat')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
# 
# app.run(debug=True, host='0.0.0.0')
