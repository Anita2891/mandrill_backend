import json

class WebSocketPublisher:
    def __init__(self):
        self.subscribers = set()

    def add_subscriber(self, subscriber):
        self.subscribers.add(subscriber)

    def remove_subscriber(self, subscriber):
        self.subscribers.remove(subscriber)

    def publish(self, event, data):
        for subscriber in self.subscribers:
            subscriber.send(json.dumps({'event': event, 'data': data}))
