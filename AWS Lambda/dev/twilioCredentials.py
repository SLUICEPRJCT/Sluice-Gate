import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Replace with your Firebase project's credentials
cred = credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sluice-gate-early-warning-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

twilioSid = input("twilio SID : ")
twilioAuthToken = input("twilio Auth Token : ")
twilioFromNumb = input("from number : ")
twilioToNumb = input("To number")

ref = db.reference()

ref.child("twilioSid").set(twilioSid)
ref.child("twilioAuthToken").set(twilioAuthToken)
ref.child("twilioFromNumb").set(twilioFromNumb)
ref.child("twilioToNumb").set(twilioToNumb)