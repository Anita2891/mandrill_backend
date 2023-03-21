from app import app
from flask import request,abort,jsonify
from app.models import madril_model as mm
from flask_socketio import SocketIO
from models.WebSocketPublisher import WebSocketPublisher as wp 
from models.WebSocketSubscriber import WebSocketSubscriber as wsub

socketio=SocketIO(app)
websocket_publisher = wp()


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    event = request.headers.get('X-Mandrill-Event')
    if event == 'inbound':
        # Handle inbound email
        pass
    elif event == 'open':
        message_id = request.json['msg']['_id']
        # Store message payload into Redis
        mm.process_event_data(request.json)

        # Publish notification that user opened email via WebSocket
        wp.publish('open', {'message_id': message_id})

    return jsonify({'status': 'success'})


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/ws')
def handle_websocket():
    ws = request.environ.get('wsgi.websocket')
    if not ws:
        abort(400, 'Expected WebSocket request.')

    # Create a WebSocket subscriber for the connection
    websocket_subscriber = wsub(ws)
    wp.add_subscriber(websocket_subscriber)

    while not ws.closed:
        # Keep connection alive
        ws.receive()

    # Remove the WebSocket subscriber when the connection is closed
    wp.remove_subscriber(websocket_subscriber)

    return 'OK'

@socketio.on('connect')
def ws_connect():
    print('Client connected')

@socketio.on('disconnect')
def ws_disconnect():
    print('Client disconnected')