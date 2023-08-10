import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Replace with your Firebase project's credentials
cred = credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sluice-gate-early-warning-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

stge3Thresh = input("stage 3 warning threshold : ")
stge2Thresh = input("stage 2 warning threshold : ")

ref = db.reference()

ref.child("stge3Thresh").set(stge3Thresh)
ref.child("stge2Thresh").set(stge2Thresh)
