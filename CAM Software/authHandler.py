import requests
from datetime import datetime, timedelta
import base64
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize Firebase Admin SDK with your credentials
cred = credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sluice-gate-early-warning-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

url = 'http://worldtimeapi.org/api/timezone/Asia/Colombo'  # You can change this to your desired timezone


def encyptTime():
    try:
        response = requests.get(url)
        data = response.json()
        current_time = datetime.fromisoformat(data['datetime'])
        formatted_time = current_time.strftime('%Y:%m:%d:%H:%M:%S')
        encrypted_time = base64.b64encode(formatted_time.encode()).decode()
        return encrypted_time
    except:
        return None


def decryptTime(encrptedTime):
    decryptedTime = base64.b64decode(encrptedTime.encode()).decode()
    return decryptedTime


def timeAuth():
    try:
        # Get a reference to the database service
        ref = db.reference('timeCheck')

        # Retrieve the value of the key
        value = ref.get()

        currentTime = decryptTime(encyptTime())
        firebaseTime = decryptTime(value)

        # Convert the datetime strings to datetime objects
        dateTimeObjCurr = datetime.strptime(currentTime, '%Y:%m:%d:%H:%M:%S')
        dateTimeObjFire = datetime.strptime(firebaseTime, '%Y:%m:%d:%H:%M:%S')

        # Calculate the time difference in minutes
        global timeDiff
        timeDiff = (dateTimeObjCurr - dateTimeObjFire).total_seconds() / 60

        # The number of minutes after which the time difference is considered "passed"
        thresholdMins = 60

        if timeDiff >= thresholdMins:
            return True
        else:
            return False
    except:
        return None


def coolDownTime():
    return int(60 - timeDiff)


def enterdPhrase(enterd):
    global ref
    ref = db.reference('oneTimeUse')
    if ref.get() is not None:
        value = ref.get()
        if enterd == value:
            ref.delete()
            return 'ok'
        else:
            return 'wrong'
    else:
        return 'used'
