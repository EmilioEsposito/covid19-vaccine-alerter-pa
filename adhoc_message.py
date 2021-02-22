import os
import sys
import datetime
import json
from twilio.rest import Client
import requests
from dateutil import parser

# control the working directory explicitly for the cron job to work properly:
os.chdir('/home/ec2-user/covid19-vaccine-alerter-pa')
os.chdir('/Users/eesposito/sandbox')

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
with open('sms_recipients.json','r') as f: # TODO: we should have this file auto-populated based off of Google Form submissions
    sms_recipients = json.load(f)
    print(sms_recipients)

account_sid = creds['TWILIO_SID']
auth_token = creds['TWILIO_AUTH']
client = Client(account_sid, auth_token)

# message = client.messages.create(
#     messaging_service_sid=creds['MESSAGING_SID'],
#     body='You have been successfully enrolled in COVID vaccine text alerts. There is no need to resubmit the Google Form. This phone number is not monitored for responses.',
#     to="+1415556666"
# )
# print(message.sid)

# define simple function that will send a SMS to each of the recipients in the sms_recipients list
def send_sms(body='', recipients=[]):

    for recipient in recipients:
        try:
            message = client.messages.create(
                messaging_service_sid=creds['MESSAGING_SID'],
                body=body,
                to=recipient
            )
            print(message.sid)
        except:
            print("Failed:", recipient)

msg = """
Current Appointment Links:
Tuesday, Feb 23
https://cw2-pennsylvania-production.herokuapp.com/reg/9812604549
Wednesday, Feb 24
https://cw2-pennsylvania-production.herokuapp.com/reg/8161405192
Thursday, Feb 25
https://cw2-pennsylvania-production.herokuapp.com/reg/1412955608
Friday, Feb 26
https://cw2-pennsylvania-production.herokuapp.com/reg/4518296012
"""
send_sms(body=msg,recipients=sms_recipients)

