import json
from flask import Flask, request
from common.utils import create_webhook
from webexteamssdk import WebexTeamsAPI, Webhook

WEBEX_TEAMS_ACCESS_TOKEN = 'YTZjNDJiYWYtZWVjZS00ZjM4LTk2NzItZmQwNzBlM2M1NGU0MTIwZDhhZTMtNWIx_P0A1_19365916-598f-457d-9ca7-51a422c8769e'

teams_api = None
allEvents = {}

app = Flask(__name__)
@app.route('/messages_webhook', methods=['POST'])
def messages_webhook():
    if request.method == 'POST':
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
        commands(command, data.personEmail, data.roomId)
        return '200'

    
def timer():
    return

def timezone():
    return

def generate_add_event_card():
    return {
    "type": "AdaptiveCard",
    "body": [
        {
            "type": "TextBlock",
            "text": "Enter name of event",
            "wrap": True
        },
        {
            "type": "Input.Text",
            "placeholder": "Event name",
            "id": "event_Name"
        },
        {
            "type": "TextBlock",
            "text": "Enter date of event",
            "wrap": True
        },
        {
            "type": "Input.Date",
            "id": "event_Date"
        },
        {
            "type": "TextBlock",
            "text": "Enter time of event",
            "wrap": True
        },
        {
            "type": "Input.Time",
            "id": "event_Time"
        },
        {
            "type": "ActionSet",
            "horizontalAlignment": "Left",
            "spacing": "None",
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Enter event"
                }
            ]
        }
    ],
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "version": "1.3"
}

def generate_reminder_card():
    return

def create_event():
    return

def view_events():
    return

def send_direct_message(person_email, message):
    teams_api.messages.create(toPersonEmail=person_email, text=message)

def send_message_in_room(room_id, message):
    teams_api.messages.create(roomId=room_id, text=message)


def commands(command, sender, roomId):
    if command == "create event":
        create_event(roomId, sender)
    elif command == "view events":
        view_events(roomId, sender)
    elif command == "help":
        send_message_in_room(roomId, "These are the commands that you can use:\n")

        

if __name__ == '__main__':
    teams_api = WebexTeamsAPI(access_token=WEBEX_TEAMS_ACCESS_TOKEN)
    create_webhook(teams_api, 'messages_webhook', '/messages_webhook', 'messages')
    create_webhook(teams_api, 'attachmentActions_webhook', '/attachmentActions_webhook', 'attachmentActions')
    app.run(host='0.0.0.0', port=12000)