from app import app
from flask import request,render_template
from app.models import madril_model as mm
import asyncio

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/mandrill-webhook', methods=['POST'])
def mandrill_webhook():
    event_payload = request.get_json()
    #message_id = event_payload["_id"]
    event_type = event_payload["event"]
    if event_type=='open':
        mm.process_event_data(event_payload)
        asyncio.mm.send_notification(event_payload)
    return render_template('index.html')
