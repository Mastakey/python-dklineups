#!/home/mastakey/python/venv/bin/python2.7
from __future__ import division
import cgi
import cgitb
cgitb.enable()
from lib.SQ3Reader import SQ3Reader
from lib.DKSalary import DKSalary
from lib.DKUtil import DKUtil
from jinja2 import Environment, PackageLoader

import pdb
import time
import os
import json
import sys

#ARGS
args = cgi.FieldStorage()
myDate = ''
try:
	myDate = args['date'].value
except KeyError:
	myDate = sys.argv[1]

#CONFIG
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
	if (playerData['time_on_ice_s'] > 1020 and playerData['fppg'] > 2.5):
		return True
	else:
		return False
#David Krejci|Patrice Bergeron|Ryan O'Reilly|Brad Marchand|Alex Ovechkin|Oliver Ekman-Larsson|Rasmus Ristolainen
#def filter(playerData):
	#if (playerData['time_on_ice_s'] > 1020 and playerData['fppg'] > 2
	#and playerData['player']!='David Krejci'
	#and playerData['player']!='Patrice Bergeron'
	#and playerData['player']!='Ryan O\'Reilly'
	#and playerData['player']!='Brad Marchand'
	#and playerData['player']!='Alex Ovechkin'
	#and playerData['player']!='Oliver Ekman-Larsson'
	#and playerData['player']!='Rasmus Ristolainen'):
#		return True#
	#else:
#		return False

sorter = 'value'
#sorter = 'value'

dkutil.generatePlayerData(myDate, '2016', filter)
dkutil.generateLineup(sorter)
