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



ref = db.reference()

ref.child("ultsnc_sens").set('')