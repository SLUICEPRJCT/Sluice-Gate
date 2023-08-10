import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from twilio.rest import Client
import json

# Replace with your Firebase project's credentials
cred = credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sluice-gate-early-warning-default-rtdb.asia-southeast1.firebasedatabase.app/'
})


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
    msg = f"sesn2 value is :{value}"
    return msg


def twilioSetup(smsTxt):
    # Replace with your Twilio account SID and auth token
    account_sid = 'AC5a2502b79e59eab635cea14f6a5863a3'
    auth_token = '29e8138a6b71948a2c2776c2a333805e'

    # Replace with your Twilio phone numbers
    from_number = '+16206590244'
    to_number = '+94784580996'

    # Send message using Twilio API
    client = Client(account_sid, auth_token)
    client.messages.create(
        from_=from_number,
        body=smsTxt,
        to=to_number
    )


def lambda_handler(event, context):
    # Retrieve the input value from Firebase
    ref = db.reference('ultsnc_sens')
    refSpec = db.reference('special')

    if refSpec.get() is None:
        pass
    else:
        #twilioSetup(refSpec.get())
        print(refSpec.get())
        refSpec.delete()

    global value
    value = ref.get()

    if int(value) <= 10:
        print('move out from homes')

    elif int(value) <= 20:
        print("be aware!")

    else:
        return {
            'statusCode': 200,
            'body': json.dumps('works fine!')
        }

    # Return
    return {
        'statusCode': 200,
        'body': json.dumps('works fine!')
    }


lambda_handler("gg", "yy")
