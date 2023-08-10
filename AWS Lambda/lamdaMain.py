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


def smsStage2():
    smsStge2Msg = db.reference("stge2Msg")
    return smsStge2Msg.get()
    # msg = "URGENT: Reservoir water level has reached 80% capacity and the sluice gate is about to be opened. Please
    # " \ "be aware of potential flooding and take necessary precautions to ensure your safety." return msg


def smsStage3():
    smsStge3Msg = db.reference("stge3Msg")
    return smsStge3Msg.get()
    # msg = "EMERGENCY: Reservoir water level has reached 90% capacity. Please evacuate your homes immediately and
    # move " \ "to higher ground or a designated safe location. This is a critical situation and your safety is of
    # utmost " \ "importance." return msg


def smsTest():
    msg = f"sesn2 value is :{value}"
    return msg


def twilioSetup(smsTxt):
    # Replace with your Twilio account SID and auth token
    account_sid = db.reference("twilioSid").get()
    auth_token = db.reference("twilioAuthToken").get()

    # Replace with your Twilio phone numbers
    from_number = db.reference("twilioFromNumb").get()
    to_number = db.reference("twilioToNumb").get()

    # Send message using Twilio API
    client = Client(account_sid, auth_token)
    client.messages.create(
        from_=from_number,
        body=smsTxt,
        to=to_number
    )


def thresholdValues(refName):
    threshRef = db.reference(refName)
    return int(threshRef.get())


def lambda_handler(event, context):
    # Retrieve the input value from Firebase
    ref = db.reference('ultsnc_sens')
    refSpec = db.reference('special')

    if refSpec.get() is None:
        pass
    else:
        twilioSetup(refSpec.get())
        refSpec.delete()

    global value
    value = ref.get()

    if value == '':
        pass

    elif int(value) <= thresholdValues("stge3Thresh"):
        twilioSetup(smsStage3())
        ref.set('')


    elif int(value) <= thresholdValues("stge2Thresh"):
        twilioSetup(smsStage2())
        ref.set('')

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

# lambda_handler("test", 'test')

# print(smsStage3())
