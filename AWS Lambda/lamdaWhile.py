import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from twilio.rest import Client
import os

# Replace with your Firebase project's credentials
cred = credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sluice-gate-early-warning-default-rtdb.asia-southeast1.firebasedatabase.app/'
})


# # Retrieve the input value from Firebase
# ref = db.reference('sens2')
# value = ref.get()


def smsW1():
    msg = "URGENT: Reservoir water level has reached 80% capacity and the sluice gate is about to be opened. Please " \
          "be aware of potential flooding and take necessary precautions to ensure your safety."
    return msg


def smsW2():
    msg = "EMERGENCY: Reservoir water level has reached 90% capacity. Please evacuate your homes immediately and move " \
          "to higher ground or a designated safe location. This is a critical situation and your safety is of utmost " \
          "importance."
    return msg


def smsTest():
    msg = "system test message please ignore this msg!"
    return msg


def twilioSetup(smsTxt):
    # Replace with your Twilio account SID and auth token
    account_sid = 'AC5a2502b79e59eab635cea14f6a5863a3'
    auth_token = '29e8138a6b71948a2c2776c2a333805e'

    # Replace with your Twilio phone numbers
    from_number = '+16206590244'
    to_number = '+94784580996'

    # Replace with your message text
    message_text = 'test from lambda aws'

    # Send message using Twilio API
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_=from_number,
        body=smsTxt,
        to=to_number
    )


# # Print the input value
# print('Input value: {}'.format(value))


def lambda_handler(event, context):
    sens2Value = db.reference("sens2")
    sens2ValuePreGet = sens2Value.get()

    while True:

        # sens2ValueCurr = db.reference("sens2")
        sens2ValueCurrGet = sens2Value.get()

        # only continue if prev. data was changed
        if sens2ValueCurrGet == sens2ValuePreGet:
            continue
        else:
            sens2ValuePreGet = sens2ValueCurrGet

        # Return message SID
        return {
            'statusCode': 200,
            'body': 'no body, only katu'
        }
