import os
import sys
import datetime
import json
from twilio.rest import Client
import requests
from dateutil import parser

# control the working directory explicitly for the cron job to work properly:
# os.chdir('/home/ec2-user/covid19-vaccine-alerter-pa')

# Import TWILIO account credentials from a twilio_creds.json file. The file contents should look like this:
# {"TWILIO_AUTH":"XXXXXXXX",
# "TWILIO_SID":"XXXXXXXX",
# "MESSAGING_SID": "XXXXXXXX"}
with open('twilio_creds.json','r') as f:
    creds = json.load(f)

# Load a list of SMS recipients from a sms_recipients.json file. The file format should look like this:
# ["+1412555666",
# "+1412555777",
# "+1412555888",
# "+1412555999"
# ]
with open('sms_recipients_TEST.json','r') as f: # TODO: we should have this file auto-populated based off of Google Form submissions
    sms_recipients = json.load(f)
    print(sms_recipients)

account_sid = creds['TWILIO_SID']
auth_token = creds['TWILIO_AUTH']
client = Client(account_sid, auth_token)


# define simple function that will send a SMS to each of the recipients in the sms_recipients list
def send_sms(body='', recipients=[]):
    for recipient in recipients:
        message = client.messages.create(
            messaging_service_sid=creds['MESSAGING_SID'],
            body=body,
            to=recipient
        )
        print(message.sid)


send_sms(body="test",recipients=sms_recipients)