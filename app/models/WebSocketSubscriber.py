
class WebSocketSubscriber:
    def __init__(self, ws):
        self.ws = ws

    def send(self, message):
        self.ws.send(message)
