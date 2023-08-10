import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize Firebase Admin SDK with your credentials
cred = credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sluice-gate-early-warning-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Get a reference to the "oneTimeUse" node
ref = db.reference('special')

# Set the value of the "oneTimeUse" node to "hi"
secretKey = input("Enter OneTime use phrase: ")
ref.set(secretKey)
