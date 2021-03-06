import os
import sys
import datetime
import json
from twilio.rest import Client
import requests
from dateutil import parser

# control the working directory explicitly for the cron job to work properly:
os.chdir('/home/ec2-user/covid19-vaccine-alerter-pa')

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

# COOLOFF PERIOD STATE - Once a text is sent, we don't want to spam them the same message every X minutes.
# cooloff_period_state=True will suppress SMS messages until the allotted time has passed.
cooloff_period_state = False
next_cooloff_period_state = False # this is used to control the cooloff_period_state of the NEXT run
try:
    with open('cooloff-until.log','r') as f:
        cooloff_time_str = f.read()
    cooloff_time = parser.parse(cooloff_time_str)
    if datetime.datetime.now()<cooloff_time:
        cooloff_period_state = True
except:
    print('Probably File not Found Error. This could be handled better.')


# define simple function that will send a SMS to each of the recipients in the sms_recipients list
def send_sms(body='', recipients=[], trigger_next_cooloff_period=True):

    if cooloff_period_state:
        body='Covid Alert Cooloff period triggered. No SMS sent.'
        print(body)
        message = client.messages.create(
            messaging_service_sid=creds['MESSAGING_SID'],
            body=body,
            to=['+14123703550']
        )
        print(message.sid)

    else:
        print(f'Sending SMS: {body}')
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


    # The state can only be flipped to True and cannot be flipped back during a run
    global next_cooloff_period_state
    if trigger_next_cooloff_period:
        next_cooloff_period_state = True


# Site 1: Allegheny County Health Department
print('Checking Allegheny County Health Department')
url = 'https://www.alleghenycounty.us/Health-Department/Resources/COVID-19/COVID-19-Vaccine-Information.aspx'
resp = requests.get(url)

# check the site for new date references:
new_dates = [
# 'January 29', 'January 31', 'February 4', 'February 5', 'February 6', 'February 7', 'February 8', 'February 14',
# 'February 15','February 16', 'February 17', 'February 18', 'February 19',
# 'February 20', 'February 21', 'February 22',
# 'February 23', 'February 24', 'February 25', 'February 26',
'February 27', 'February 28', 'February 29',
'March 1 ', 'March 2 ', 'March 1,', 'March 2,', 'March 1.', 'March 2.',
'March 3', 'March 4', 'March 5', 'March 6', 'March 7', 'March 8', 'March 9',
'March 10', 'March 11', 'March 12', 'March 13', 'March 14', 'March 15', 'March 16',
'March 17', 'March 18', 'March 19', 'March 20', 'March 21', 'March 22', 'March 23', 'March 24',
'March 25', 'March 26', 'March 27', 'March 28', 'March 29', 'March 30', 'March 31'
]

for new_date in new_dates:
    msg = f'From Emilio Vaccine Alert: Potential vaccine appt available from Allegheny Health for {new_date} was just added: {url}'
    if new_date in resp.text:
        send_sms(body=msg, recipients=sms_recipients)
    # else:
    #     print('No vaccine appointment links added.')

# Site 2: Armstrong Center for Medicine & Health
print('Checking Armstrong Center for Medicine & Health')
url = 'https://api.appointlet.com/organizations/120454/scheduler'
resp = requests.get(url)
import re
x = re.findall(r'acmh-covid-vaccine.*?}',resp.text, re.DOTALL)
if 'true' in x:
    url = 'https://acmh.appointlet.com/'
    msg = f'From Emilio Vaccine Alert: Armstrong Hospital appointments may now be available: {url}'
    print(msg)
    send_sms(body=msg, recipients=sms_recipients)


# Site 3: Giant Eagle
# print('Checking Giant Eagle')
# url = 'https://sr.reportsonline.com/sr/gianteagle/immunizations'
# resp = requests.get(url)
# no_vaccine_msg = 'There are currently no COVID-19 vaccine appointments available'
# waiting_page = 'Your estimated wait time is:'
# event_ended = 'The event has ended'
# if no_vaccine_msg in resp.text:
#     print('Giant Eagle '+no_vaccine_msg)
# # elif waiting_page in resp.text:
# #     print('Giant Eagle '+waiting_page)
# elif event_ended in resp.text:
#     print('Giant Eagle '+event_ended)
# else:
#     msg = f'From Emilio Vaccine Alert: Some appointments may have just opened at Giant Eagle: {url}'
#     send_sms(body=msg, recipients=sms_recipients)
#     # send_sms(body='Prior text was a false alarm.', recipients=sms_recipients)


# Site 4: Riteaid
# print('Checking Riteaid')
# url = 'https://sr.reportsonline.com/sr/riteaid/PS2021'
# resp = requests.get(url)
# no_vaccine_msg = 'There are currently no COVID vaccine appointments available. Please check back tomorrow as we continue to add availability.'
# waiting_page = 'Your estimated wait time is:'
# event_ended = 'The event has ended'
# if no_vaccine_msg in resp.text:
#     print('RiteAid '+no_vaccine_msg)
# elif waiting_page in resp.text:
#     print('RiteAid '+waiting_page)
# elif event_ended in resp.text:
#     print('RiteAid '+event_ended)
# else:
#     msg = f'From Emilio Vaccine Alert: Potential vaccine appt available at RiteAid: {url}'
#     send_sms(body=msg, recipients=sms_recipients)
#     # send_sms(body='Prior text was a false alarm.', recipients=sms_recipients)

# LOGGING
# keep a a simple log of runtimes
now = datetime.datetime.now()
with open('covid19-vaccine-alerter-pa-runtimes.log', 'a') as f:
    output = str(now) + "\n"
    f.write(output)

# Send Emilio a daily text so he knows the script is still running, even if there are no new alerts:
print('Current Time on EC2:',now)
print(now.hour)
msg = f'COVID Vaccine Checker still running.'
if now.hour==22 and now.minute<=10:
    send_sms(body=msg, recipients=['+14123703550'], trigger_next_cooloff_period=False)

# Cooloff period file reset
if next_cooloff_period_state:
    three_hours_from_now = now+datetime.timedelta(hours=3)
    with open('cooloff-until.log','w') as f:
        f.write(str(three_hours_from_now))
