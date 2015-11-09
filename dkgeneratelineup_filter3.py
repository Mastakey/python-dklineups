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

#def filter(playerData):
#Joe Pavelski|Nathan MacKinnon|Kris Versteeg|Joel Ward|Jarome Iginla|Justin Faulk|Brent Burns
#Jason Spezza|Tyler Seguin|Dustin Brown|Tyler Toffoli|Jamie Benn|Jason Demers|Mark Streit|
#David Krejci|Leon Draisaitl|Jamie Benn|Brad Marchand|Vladimir Tarasenko|Brent Burns|Colton Parayko
#Bryan Little|Nazem Kadri|Jaromir Jagr|Vladimir Tarasenko|Patrick Kane|Colton Parayko|Morgan Rielly|
#Joe Pavelski|David Krejci|Mike Hoffman|Brad Marchand|Ryan Suter|Brent Burns|Joel Ward|Tobias Rieder
#Tyler Seguin|Leon Draisaitl|Taylor Hall|Patrick Kane|Mike Cammalleri|Jason Demers|Brent Seabrook|
#David Krejci|Evgeny Kuznetsov|Mike Hoffman|Brad Marchand|Vladimir Tarasenko|Colton Parayko|Brent Burns|
#Leon Draisaitl|Tyler Seguin|Taylor Hall|Patrick Kane|Brad Marchand|Brent Seabrook|Colin Miller|
def filter(playerData):
	if (playerData['time_on_ice_s'] > 920 and playerData['fppg'] > 2.0
	and playerData['player']!='Leon Draisaitl'
	and playerData['player']!='Tyler Seguin'
	and playerData['player']!='Taylor Hall'
	and playerData['player']!='Patrick Kane'
	and playerData['player']!='Brad Marchand'
	and playerData['player']!='Brent Seabrook'
	and playerData['player']!='Colin Miller'
	and playerData['player']!='Damon Severson'):
		return True#
	else:
		return False

sorter = 'fppg'
#sorter = 'value'

dkutil.generatePlayerData(myDate, '2016', filter)
dkutil.generateLineup(sorter)
