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
dkutil = DKUtil(sq3reader, player_list, boxscores, dkdata, {'logging':'on'})

#def filter(playerData):
#Joe Pavelski|Nathan MacKinnon|Kris Versteeg|Joel Ward|Jarome Iginla|Justin Faulk|Brent Burns
#Jason Spezza|Tyler Seguin|Dustin Brown|Tyler Toffoli|Jamie Benn|Jason Demers|Mark Streit|
#David Krejci|Leon Draisaitl|Jamie Benn|Brad Marchand|Vladimir Tarasenko|Brent Burns|Colton Parayko
#Bryan Little|Nazem Kadri|Jaromir Jagr|Vladimir Tarasenko|Patrick Kane|Colton Parayko|Morgan Rielly|
#Joe Pavelski|David Krejci|Mike Hoffman|Brad Marchand|Ryan Suter|Brent Burns|Joel Ward|Tobias Rieder
#Tyler Seguin|Leon Draisaitl|Taylor Hall|Patrick Kane|Mike Cammalleri|Jason Demers|Brent Seabrook|
#David Krejci|Evgeny Kuznetsov|Mike Hoffman|Brad Marchand|Vladimir Tarasenko|Colton Parayko|Brent Burns|
#Leon Draisaitl|Tyler Seguin|Taylor Hall|Patrick Kane|Brad Marchand|Brent Seabrook|Colin Miller|
#Tyler Seguin|Jeff Carter|Kyle Palmieri|Mike Cammalleri|James Neal|Colton Parayko|Justin Faulk|Evgeny Kuznetsov
#Leon Draisaitl|Ryan Nugent-Hopkins|Taylor Hall|Brendan Gallagher|Max Pacioretty|Andrei Markov|P.K. Subban|
#Leon Draisaitl|Martin Hanzal|Brad Marchand|Patrick Kane|Alex Ovechkin|Oliver Ekman-Larsson|Colton Parayko|
#Boone Jenner|Evgeny Kuznetsov|Joel Ward|Alex Ovechkin|Justin Williams|Brent Burns|David Savard|
#David Krejci|Leon Draisaitl|Jason Zucker|Taylor Hall|Patrick Kane|Brent Burns|Colton Parayko
#Sean Monahan|Nazem Kadri|Artemi Panarin|Patrick Kane|Mats Zuccarello|Brent Seabrook|Morgan Rielly|
#Martin Hanzal|Bryan Little|Daniel Sedin|Brendan Gallagher|Vladimir Tarasenko|Justin Faulk|Colton Parayko|

def filter(playerData):
	if (playerData['time_on_ice_s'] > 900 and playerData['fppg'] > 2.0
	and playerData['player']!='Martin Hanzal'
	and playerData['player']!='Bryan Little'
	and playerData['player']!='Daniel Sedin'
	and playerData['player']!='Brendan Gallagher'
	and playerData['player']!='Vladimir Tarasenko'
	and playerData['player']!='Justin Faulk'
	and playerData['player']!='Colton Parayko'
	and playerData['player']!='Mikkel Boedker'):
		return True#
	else:
		return False

sorter = 'fppg'
#sorter = 'value'

dkutil.generatePlayerData(myDate, '2016', filter)
dkutil.generateLineup_v2(sorter)
