import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Replace with your Firebase project's credentials
cred = credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sluice-gate-early-warning-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

stge3Msg = input("stage 3 warning msg : ")
stge2Msg = input("stage 2 warning msg : ")

ref = db.reference()

ref.child("stge3Msg").set(stge3Msg)
ref.child("stge2Msg").set(stge2Msg)
