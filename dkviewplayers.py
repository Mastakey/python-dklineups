#!/home/mastakey/python/venv/bin/python2.7
from __future__ import division
import cgi
import cgitb
cgitb.enable()
from operator import itemgetter
from lib.SQ3Reader import SQ3Reader
from lib.DKSalary import DKSalary
from lib.DKUtil import DKUtil
from jinja2 import Environment, PackageLoader

import pdb
import time
import os
import json
import itertools
import sys

#HTML Header
print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

#ARGS
args = cgi.FieldStorage()
myDate = ''
try:
	myDate = args['date'].value
except KeyError:
	myDate = sys.argv[1]

myPosition = ''
try:
	myPosition = args['position'].value
except KeyError:
	myPosition = sys.argv[2]

#CONFIG
env = Environment(loader=PackageLoader('tmpl', ''))
template = env.get_template('body/players_by_date_with_stats_json.html')
player_stats_sorted=[]
json_player_data=[]

myYear = '2016'
#myDate = '2015-10-28'

#MAIN
#GET All players for the year
myPlayers = []
sq3reader = SQ3Reader('db/'+myDate+'_boxscores.db', {'logging':'off'})
player_list = sq3reader.executeQueryDict("""SELECT distinct d.player, d.team
		from boxscore_data d, boxscore b WHERE d.boxscore = b.id
		AND b.season='"""+myYear+"""'
		""")
#print len(player_list)
boxscores = sq3reader.executeQueryDict("""SELECT id, vteamstr, hteamstr
		from boxscore where gamedate='"""+myDate+"""'
		""")
#GET DK Salary
dksalary = DKSalary('input/'+myDate+'_DKSalaries.csv')
dkdata = dksalary.getDkdata()

#Load DK UTIL
dkutil = DKUtil(sq3reader, player_list, boxscores, dkdata, {'logging':'off'})

def filter(playerData):
	#if playerData['time_on_ice_s'] > 720 and playerData['fppg'] > 2 and playerData['player']!='Mike Hoffman' and playerData['player']!='Evgeny Kuznetsov' and playerData['player']!='Nicklas Backstrom':
	#	return True
	#else:
	#	return False
	return True
dkutil.generatePlayerData(myDate, '2016', filter)

player_stats = dkutil.getPlayerStats(myPosition)
json_player_data = json.dumps(player_stats)

player_stats_sorted = sorted(player_stats, key=itemgetter('time_on_ice_s'), reverse=True)
print template.render(player_stats=player_stats_sorted, json_player_data=json_player_data, date=myDate, position=myPosition)
