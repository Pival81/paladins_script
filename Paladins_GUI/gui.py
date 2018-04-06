#!/bin/env python

import sys
from PyQt5.QtWidgets import *
import requests
from datetime import datetime
import json
from hashlib import md5
import time

devid = "2518"
authkey = "BF4E10BFD82145C89BFB4340F26754EA"

# def timeformat(buh):
# 	i = datetime.strptime(buh, '%m/%d/%Y %I:%M:%S %p')
# 	i = i + (datetime.now() - datetime.utcnow())
# 	i= i.strftime('%d/%m/%Y %I:%M:%S %p')
# 	return i

def timestamp ():
	timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
	return timestamp

def signature (method):
	signature = devid + method + authkey + timestamp()
	signature = md5(signature.encode('utf-8')).hexdigest()
	return signature

def createsession():
	with open("sessions.json") as sessions_file:
		sessions = json.load(sessions_file)
	if (time.time() - sessions["epoch"]) < 900:
		session_id = sessions["session_id"]
	else:
		request = requests.get('http://api.paladins.com/paladinsapi.svc/createsessionJson' + '/' + devid + '/' + signature("createsession") + '/' + timestamp())
		request = json.loads(request.text)
		session_id = request["session_id"]
	data = {"session_id": session_id, "epoch": time.time()}
	with open("sessions.json", "w") as sessions_file:
		sessions_file.write(json.dumps(data, indent=4, sort_keys=True, separators=(',', ': ')))
	return session_id

def getplayer(print_data, player):	
	playerinfo = requests.get("http://api.paladins.com/paladinsapi.svc/getplayerJson/" + devid + '/' + signature("getplayer") + '/' + createsession() + '/' + timestamp() + '/' + player)
	playerinfo_json = json.loads(playerinfo.text)[0]
	if print_data == 1:
		print("Level:", playerinfo_json["Level"])
		print("Wins:", playerinfo_json["Wins"])
		print("Losses:", playerinfo_json["Losses"])
		print("Region:", playerinfo_json["Region"])
		print("Creation date:", timeformat(playerinfo_json["Created_Datetime"]))
		print("Last login:", timeformat(playerinfo_json["Last_Login_Datetime"]))
	return playerinfo_json


class App(QMainWindow):
	
	def __init__(self):
		super().__init__()
		
		self.initUI()
		
		
	def initUI(self):

		self.setGeometry(300,300,350,100)
		self.setFixedSize(350, 70)
		self.setWindowTitle("Paladins_Test")

		self.hbox = QHBoxLayout()
		self.vbox = QVBoxLayout()
		self.vbox.addLayout(self.hbox)

		window = QWidget()
		window.setObjectName("mainwidget")
		window.setLayout(self.vbox)
		self.setCentralWidget(window)

		self.textbox = QLineEdit(self)
		self.button = QPushButton("Submit", self)

		self.button.clicked.connect(self.showTabs)
		self.textbox.returnPressed.connect(self.button.click)

		self.hbox.addWidget(self.textbox)
		self.hbox.addWidget(self.button)



	def showTabs(self):
		self.setFixedSize(350, 500)
		player = self.textbox.text()
		tabwidget = QTabWidget(self)

		self.vbox.addWidget(tabwidget)

		tab1 = QWidget(self)
		tab1.layout = QVBoxLayout()

		tab1.setLayout(tab1.layout)
		tabwidget.addTab(tab1, "Player Info")

		playerinfo = getplayer(0, player)

		label1 = QLabel(self)
		label1.setText(str(playerinfo["Name"]))
		label1.setObjectName("playername")

		label2 = QLabel(self)
		label2.setText("Level:" + " " + str(playerinfo["Level"]) )

		label3 = QLabel(self)
		label3.setText("Wins:" + " " + str(playerinfo["Wins"]) )

		label4 = QLabel(self)
		label4.setText("Losses:" + " " + str(playerinfo["Losses"]) )

		label5 = QLabel(self)
		label5.setText("Region:" + " " + str(playerinfo["Region"]) )

		tab1.layout.addWidget(label1)
		tab1.layout.addWidget(label2)
		tab1.layout.addWidget(label3)
		tab1.layout.addWidget(label4)
		tab1.layout.addWidget(label5)
		tab1.layout.addStretch(1)


if __name__ == '__main__':
    
	app = QApplication(sys.argv)
	gui = App()

	with open('style.qss', 'r') as myfile:
		qss = myfile.read()

	app.setStyleSheet(qss)
	gui.show()
	sys.exit(app.exec_())