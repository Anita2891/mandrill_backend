from flask_socketio import SocketIO
from app import app
import redis
import json
import websockets

redis_client = redis.Redis(host='localhost', port=6379, db=0)

socketio = SocketIO(app)

async def send_notification(payload):
    async with websockets.connect('ws://localhost:8000') as websocket:
        # Send message payload to WebSocket client
        await websocket.send(json.dumps({'type': 'notification', 'message': payload['msg']}))


def process_event_data(data):
    event_type = data['event']
    message_id = data['msg']['_id']
    email = data['msg']['email']
    timestamp = data['ts']
    redis_client.hset(message_id, 'event_type', event_type)
    redis_client.hset(message_id, 'email', email)
    redis_client.hset(message_id, 'timestamp', timestamp)
    redis_client.set(message_id,data)

def get_redis_data(message_id):
    return redis_client.get(message_id)
