import requests
from datetime import datetime
import json
from hashlib import md5
import time

devid = "2518"
authkey = "BF4E10BFD82145C89BFB4340F26754EA"

def timeformat(buh):
	i = datetime.strptime(buh, '%m/%d/%Y %I:%M:%S %p')
	i = i + (datetime.now() - datetime.utcnow())
	i= i.strftime('%d/%m/%Y %I:%M:%S %p')
	return i

def timestamp ():
	timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
	return timestamp

def signature (method):
	signature = devid + method + authkey + timestamp()
	signature = md5(signature.encode('utf-8')).hexdigest()
	return signature

def getfriends():
	getfriends = requests.get("http://api.paladins.com/paladinsapi.svc/getfriendsJson/" + devid + '/' + signature("getfriends") + '/' + session_id + '/' + timestamp() + '/' + player)
	getfriends = json.loads(getfriends.text)
	friends = [friend["name"] for friend in getfriends]
	for i in friends:
		friend_status = requests.get("http://api.paladins.com/paladinsapi.svc/getplayerstatusJson/" + devid + '/' + signature("getplayerstatus") + '/' + session_id + '/' + timestamp() + '/' + i)
		friend_status = json.loads(friend_status.text)[0]
		# for n in friend_status:
		# 	n.replace("God", "Champion")
		print("----------------------------------------")
		print(i) 
		print(friend_status["status_string"])

def getmatchhistory():
	getmatchhistory = requests.get("http://api.paladins.com/paladinsapi.svc/getmatchhistoryJson/" + devid + '/' + signature("getmatchhistory") + '/' + session_id + '/' + timestamp() + '/' + player)
	getmatchhistory = json.loads(getmatchhistory.text)
	print(getmatchhistory)

def getplayer(print_data):	
	playerinfo = requests.get("http://api.paladins.com/paladinsapi.svc/getplayerJson/" + devid + '/' + signature("getplayer") + '/' + session_id + '/' + timestamp() + '/' + player)
	print(playerinfo.headers)
	playerinfo_json = json.loads(playerinfo.text)[0]
	if print_data == 1:
		print("Level:", playerinfo_json["Level"])
		print("Wins:", playerinfo_json["Wins"])
		print("Losses:", playerinfo_json["Losses"])
		print("Region:", playerinfo_json["Region"])
		print("Creation date:", timeformat(playerinfo_json["Created_Datetime"]))
		print("Last login:", timeformat(playerinfo_json["Last_Login_Datetime"]))
	return playerinfo_json

def getchampionranks():
	playerchamps = requests.get("http://api.paladins.com/paladinsapi.svc/getchampionranksJson/" + devid + '/' + signature("getchampionranks") + '/' + session_id + '/' + timestamp() + '/' + player)
	playerchamps_json = json.loads(playerchamps.text)
	for champ in playerchamps_json:
		print("Champion:", champ["champion"])
		print("Rank:", champ["Rank"])
		print("Wins:", champ["Wins"])
		print("Losses:", champ["Losses"])
		print("Kills:", champ["Kills"])
		print("Deaths:", champ["Deaths"])
		print("Assists:", champ["Assists"])
		print("----------------------------------------")

def buh():
	getplayer(0)
	getplayerloadouts = requests.get("http://api.paladins.com/paladinsapi.svc/getplayerloadoutsJson/" + devid + '/' + signature("getplayerloadouts") + '/' + session_id + '/' + timestamp() + '/' + str(playerinfo["Id"]) + '/' + "1")
	getplayerloadouts = json.loads(getplayerloadouts.text)
	print(getplayerloadouts)

def getdataused():
	getdataused = requests.get("http://api.paladins.com/paladinsapi.svc/getdatausedJson/" + devid + '/' + signature("getdataused") + '/' + session_id + '/' + timestamp())
	getdataused = json.loads(getdataused.text)[0]
	print("Total sessions today:", getdataused["Total_Sessions_Today"])
	print("Active sessions:", getdataused["Active_Sessions"])
	print("Total requests today:", getdataused["Total_Requests_Today"])


print("Enter the player name:")
player = input(">> ")
while True:
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

	print("These are the available functions:")
	print("1) /getfriends")
	print("2) /getmatchhistory")
	print("3) /getplayerloadouts")
	print("4) /getplayer")
	print("5) /getchampionranks")
	print("6) /getdataused")
	print("7) exit")
	print("")
	action = int(input(">> "))
	if action == 1:
		getfriends()
	elif action == 2:
		getmatchhistory()
	elif action == 3:
		buh()
	elif action == 4:
		getplayer(1)
	elif action == 5:
		getchampionranks()
	elif action == 6:
		getdataused()
	elif action == 7:
		exit()
	time.sleep(2)
	print("")
