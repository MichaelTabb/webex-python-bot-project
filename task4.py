import json
from common.poll import Poll
from datetime import time, datetime
from flask import Flask, request
from common.utils import create_webhook
from webexteamssdk import WebexTeamsAPI, Webhook

WEBEX_TEAMS_ACCESS_TOKEN = 'ZWY5OTY2ZDMtNzc2My00ZWVmLWIyNmMtYzc2ZTg5M2ZkM2I3MThhNzlkMmMtZTBm_P0A1_19365916-598f-457d-9ca7-51a422c8769e'

teams_api = None
all_events = {}

app = Flask(__name__)
@app.route('/messages_webhook', methods=['GET'])
def messages_webhook():
    if request.method == 'GET':
        webhook_obj = Webhook(request.json)
        return process_message(webhook_obj.data)
    
def process_message(data):
    if data.personId == teams_api.people.me().id:
        # Message sent by bot, do not respond
        return '200'
    else:
        message = teams_api.messages.get(data.id).text
        print(message)
        commands_split = (message.split())[1:]
        command = ' '.join(commands_split)
        parse_message(command, data.personEmail, data.roomId)
        return '200'

def parse_message(command, sender, roomId):
    if command == "create event":
        create_event(roomId, sender)
    elif command == "view events":
        if all_events[roomId]:
            view_events(roomId, sender)
    
def timer(time_Hours, time_Minutes, time_Seconds):
    total_seconds = int(time_Hours) * 3600 + int(time_Minutes) * 60 + int(time_Seconds)
    while total_seconds > 0:
        timer = datetime.timedelta(seconds = total_seconds)
        time.sleep(1)
        total_seconds -= 1
    return

def generate_add_event_card(roomId):
    return {
    "type": "AdaptiveCard",
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "version": "1.3",
    "body": [
        {
            "type": "TextBlock",
            "text": "Create a Reminder",
            "wrap": True,
            "size": "Large"
        },
        {
            "type": "TextBlock",
            "text": "What is the name of the event?",
            "wrap": True
        },
        {
            "type": "Input.Text",
            "placeholder": "Event Name",
            "id": "event_Name"
        },
        {
            "type": "TextBlock",
            "text": "How long till the event?",
            "wrap": True
        },
        {
            "type": "Input.Text",
            "placeholder": "Hours",
            "id": "time_Hours",
            "isRequired": True,
            "label": "Enter an Integer Number",
            "errorMessage": "Not an integer number"
        },
        {
            "type": "Input.Text",
            "placeholder": "Minutes",
            "id": "time_Minutes",
            "isRequired": True,
            "label": "Enter an Integer Number",
            "errorMessage": "Not an integer number"
        },
        {
            "type": "Input.Text",
            "placeholder": "Seconds",
            "id": "time_Seconds",
            "label": "Enter an Integer Number",
            "errorMessage": "Not an integer number",
            "isRequired": True
        },
        {
            "type": "Input.Text",
            "id": "roomId",
            "value": roomId,
            "isVisible": False
        },
        {
            "type": "ActionSet",
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Submit"
                }
            ]
        }
    ]
}

def generate_reminder_card(roomId):
    return

def create_event(roomId, sender):
    teams_api.messages.create(toPersonEmail=sender, text="Cards Unsupported", attachments=[generate_add_event_card(roomId)])

def send_reminder(roomId, sender, timer):
    teams_api.messages.create(toPersonEmail=sender, text="Cards Unsupported", attachments=[generate_reminder_card(roomId)])

def view_events():
    return

def send_direct_message(person_email, message):
    teams_api.messages.create(toPersonEmail=person_email, text=message)

def send_message_in_room(room_id, message):
    teams_api.messages.create(roomId=room_id, text=message)


@app.route('/attachmentActions_webhook', methods=['POST'])
def attachmentActions_webhook():
    if request.method == 'POST':
        print("attachmentActions POST!")
        webhook_obj = Webhook(request.json)
        return process_card_response(webhook_obj.data)

def process_card_response(data):
    attachment = (teams_api.attachment_actions.get(data.id)).json_data
    inputs = attachment['inputs']
    if 'event_Name' in list(inputs.keys()):
        add_event(inputs['event_Name'], inputs['time_Hours'], inputs['time_Minutes'], inputs['time_Seconds'], inputs['roomId'], teams_api.people.get(data.personId).emails[0])
        send_message_in_room(inputs['roomId'], "Reminder created with title: " + inputs['event_Name'])
    return '200'

def add_event(event_Name, time_Hours, time_Minutes, time_Seconds, room_id, author):
    print(author)
    event = (event_Name, time_Hours, time_Minutes, time_Seconds, room_id, author)
    all_events[room_id] = event


if __name__ == '__main__':
    teams_api = WebexTeamsAPI(access_token=WEBEX_TEAMS_ACCESS_TOKEN)
    create_webhook(teams_api, 'messages_webhook', '/messages_webhook', 'messages')
    create_webhook(teams_api, 'attachmentActions_webhook', '/attachmentActions_webhook', 'attachmentActions')
    app.run(host='0.0.0.0', port=12000)