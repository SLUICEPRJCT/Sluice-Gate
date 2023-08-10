import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime, timedelta
import requests
import base64

# Initialize Firebase Admin SDK with your credentials
cred = credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sluice-gate-early-warning-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

url = 'http://worldtimeapi.org/api/timezone/Asia/Colombo'  # You can change this to your desired timezone


def encyptTime():
    response = requests.get(url)
    data = response.json()
    current_time = datetime.fromisoformat(data['datetime'])
    formatted_time = current_time.strftime('%Y:%m:%d:%H:%M:%S')
    encrypted_time = base64.b64encode(formatted_time.encode()).decode()
    return encrypted_time


db.reference().child("timeCheck").set(encyptTime())
