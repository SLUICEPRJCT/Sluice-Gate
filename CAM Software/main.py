from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
import sys
import serial
import hashCheck
import authHandler
import serial.tools.list_ports
import requests

loader = QUiLoader()

app = QtWidgets.QApplication(sys.argv)
mainWind = loader.load('main.ui', None)
loginWind = loader.load('login.ui', None)
warningWind = loader.load('warning.ui', None)
okWind = loader.load('ok.ui', None)

# warningWindMsg = "WARNING: You have already used the emergency SMS alert system.\nTo prevent spam and misuse,
# " \ "there is a cooldown period of one hour.\nHowever, if you have a one-time use special key, " \ "you can enter
# it below to gain access to the system in case of a more urgent emergency.\nOtherwise, " \ "please wait {} minutes
# before trying again."


def login():
    loginWind.statusLabel.setText('')
    try:
        response = requests.get("https://www.google.com")
        if response.status_code == 200:
            loginWind.statusLabel.setText('Connection Check Done...')
    except:
        loginWind.statusLabel.setText('Check Your Connection...')
        print("Internet connection not available.")
        return

    username = loginWind.userName.text()
    password = loginWind.userPassword.text()
    if hashCheck.login(username, password) == "success":
        authHandlerStat = authHandler.timeAuth()
        if authHandlerStat is True:
            mainWind.show()
            loginWind.close()
        elif authHandlerStat is False:
            warningWind.show()
            warnMsg = "WARNING: You have already used the emergency SMS alert system. \n"\
                      f"please wait {authHandler.coolDownTime()} minutes before trying again."

            warningWind.label.setText(warnMsg)
            warningWind.pushButton.clicked.connect(closeWarningWind)
            warningWind.oneTimeButton.clicked.connect(checkOneTimePhrase)

            loginWind.close()
            print(f"remaing time : {authHandler.coolDownTime()}")
        else:
            loginWind.statusLabel.setText('Connection error, try again...')

    else:
        loginWind.userName.setText('')
        loginWind.userPassword.setText('')
        loginWind.statusLabel.setStyleSheet("color: red;")
        loginWind.statusLabel.setText('Username or password incorrect!')
        # password eka waradi kyala dapan


loginWind.loginButton.clicked.connect(login)

def closeWarningWind():
    warningWind.close()


def boardConnect():
    global nodeMcuBoard
    global connected
    if detectBoard() == "notFound":
        # board eka plug karanna kyapan
        mainWind.textBrowserStatus.setText('Device connection failed...')
        mainWind.textBrowserStatus.setStyleSheet("color: yellow;")
        pass
    portDetail = detectBoard()
    try:
        nodeMcuBoard = serial.Serial(portDetail, 115200)
        # while True:
        #     ardRead = nodeMcuBoard.readline().decode().strip()
        #     mainWind.textBrowserStatus.setText(ardRead)
        #     print("aaaaa")
        #     if ardRead == "Connected":
        #         break
    except:
        # mainWind.textBrowserStatus.setText('Wrong Port or Board Not Connected!')
        return

    mainWind.sendButton.clicked.connect(sendData)
    mainWind.textBrowserStatus.setText('Connected!')
    mainWind.textBrowserStatus.setStyleSheet("color: lime;")


def sendData():
    mainWind.textBrowserStatus.setText('Sending data...')
    getData = mainWind.sendTextEdit.toPlainText()
    timeCheck = authHandler.encyptTime()
    if timeCheck is None:
        mainWind.textBrowserStatus.setText('Connection error, try again...')
        mainWind.textBrowserStatus.setStyleSheet("color: red;")
        return
    addingLine = "special^" + "Message From Sluice Gate Control System: " + getData + "#timeCheck^" + str(timeCheck) + "\n"
    print(addingLine)
    nodeMcuBoard.write(addingLine.encode())
    nodeMcuBoard.close()
    mainWind.close()
    okWind.show()
    okWind.okButton.clicked.connect(okWind.close)


# Connect boardConnectButton to boardConnect function
mainWind.boardConnectButton.clicked.connect(boardConnect)
mainWind.closeButton.clicked.connect(mainWind.close)


def detectBoard():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if "Silicon Labs CP210x" in p.description:
            return p.device
    return "notFound"


def checkOneTimePhrase():
    enterdValue = warningWind.plainTextEdit.toPlainText()
    if authHandler.enterdPhrase(enterdValue) == 'ok':
        loginWind.close()
        warningWind.close()
        mainWind.show()
    elif authHandler.enterdPhrase(enterdValue) == 'used':
        warningWind.plainTextEdit.setPlainText('')
        warningWind.label.setText('INVALID KEY: The one-time use special key you entered is invalid or, \n'
                                  'has already been used.\n'
                                  f'Wait {authHandler.coolDownTime()} minutes before trying again. ')
        # eeka use kala kyala kypn
    elif authHandler.enterdPhrase(enterdValue) == 'wrong':
        warningWind.plainTextEdit.setPlainText('')
        warningWind.label.setText('INVALID KEY: The one-time use special key you entered is invalid or, \n'
                                  'has already been used.\n'
                                  f'Wait {authHandler.coolDownTime()} minutes before trying again. ')
        # oninam kypn eeka waradi kyala


# Show the main window and start the event loop
# mainWind.show()
loginWind.show()
app.exec()
