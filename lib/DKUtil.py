import SQ3Reader
import math
from operator import itemgetter
import itertools
import sys

class DKUtil(object):
    def __init__(self, sq3, players_list, boxscores, salary_data, config):
        self.sq3 = sq3
        self.players_list = players_list
        self.boxscores = boxscores
        self.salary_data = salary_data
        self.todays_players = DKUtil.getTodaysPlayersFromTeam(players_list, boxscores)
        self.player_stats = []
        self.center_stats = []
        self.wing_stats = []
        self.defence_stats = []
        self.config = config

    def debugLog(self, string):
        if self.config['logging'] == "on":
            f = open("DKUtil.log", "a")
            f.write(str(string).encode('utf8'))
            f.write("\n")

    def generateLineup_v2(self, sorter):
        mylineup_center = [list(x) for x in itertools.combinations(self.center_stats, 2)]
        mylineup_wing = [list(x) for x in itertools.combinations(self.wing_stats, 3)]
        mylineup_defence = [list(x) for x in itertools.combinations(self.defence_stats, 2)]
        myset = []
        myset.append(mylineup_center)
        myset.append(mylineup_wing)
        myset.append(mylineup_defence)
        mycombos = itertools.product(*myset)
        mylineups = []
        mycount = 0
        for combo in mycombos:

        #for myc in mylineup_center:
        #    for myw in mylineup_wing:
        #        for myd in mylineup_defence:
                    #lineup = []
                    #lineup.extend(myc)
                    #lineup.extend(myw)
                    #lineup.extend(myd)
            for lineup in combo:
                salary = 0
                fppg = 0.0
                lineupstr = ""
                for player in lineup:
                    salary += int(player['salary'])
                    fppg += float(player['fppg'])
                    lineupstr += player['player']+"|"
                if salary < 40000:
                    myvalue = fppg/salary
                    mydict = {'lineup':lineupstr, 'salary':salary, 'fppg':fppg, 'value':myvalue}
                    mylineups.append(mydict)
                if mycount % 10000 == 0:
                    #print mycount
                    sys.stdout.flush()
                mycount += 1

        mylineups = sorted(mylineups, key=itemgetter(sorter), reverse=True)
        for myl in mylineups:
            print str(myl['fppg'])+","+str(myl['salary'])+","+str(myl['value'])+","+myl['lineup']

    def generateLineup(self, sorter):
        mylineup_center = [list(x) for x in itertools.combinations(self.center_stats, 2)]
        mylineup_wing = [list(x) for x in itertools.combinations(self.wing_stats, 3)]
        mylineup_defence = [list(x) for x in itertools.combinations(self.defence_stats, 2)]
        mylineups = []
        for myc in mylineup_center:
            for myw in mylineup_wing:
                for myd in mylineup_defence:
                    lineup = []
                    lineup.extend(myc)
                    lineup.extend(myw)
                    lineup.extend(myd)
                    salary = 0
                    fppg = 0
                    lineupstr = ''
                    for player in lineup:
                        salary += int(player['salary'])
                        fppg += float(player['fppg'])
                        lineupstr += player['player']+"|"
                    if salary < 40000:
                        myvalue = fppg/salary
                        mydict = {'lineup':lineupstr, 'salary':salary, 'fppg':fppg, 'value':myvalue}
                        mylineups.append(mydict)

        mylineups = sorted(mylineups, key=itemgetter(sorter), reverse=True)
        for myl in mylineups:
            print str(myl['fppg'])+","+str(myl['salary'])+","+str(myl['value'])+","+myl['lineup']



    def getTodaysPlayers(self):
        return self.todays_players
    def getPlayerStats(self, position):
        if position == 'C':
            return self.center_stats
        elif position == 'W':
            return self.wing_stats
        elif position == 'D':
            return self.defence_stats
        else:
            return self.player_stats

    def generatePlayerData(self, date, season, restrictions):
        for p in self.todays_players:
            player = {}
            playerName = p['player'].replace('\'', '\'\'')
            #self.debugLog("Player:")
            self.debugLog(playerName)
            salary = DKUtil.getPlayerSalary(p['player'], self.salary_data)
            position = DKUtil.getPlayerPosition(p['player'], self.salary_data)
            #self.debugLog("Salary:")
            #self.debugLog(salary)
            #self.debugLog("Position:")
            #self.debugLog(position)
            player_data = DKUtil.getDBPlayerData(self.sq3, playerName, season)
            #self.debugLog("Player Data:")
            #self.debugLog(player_data)
            data = DKUtil.getPlayerSummaryStats(p['player'], p['team'], player_data)
            #self.debugLog("Stats Data:")
            #self.debugLog(data)
            oppteams = DKUtil.getOppTeams(self.sq3, p['team'], date)
            data['position'] = position
            data['salary'] = salary
            data['vteam'] = oppteams[0]['vteamstr']
            data['hteam'] = oppteams[0]['hteamstr']
            #print type(salary)
            #self.debugLog("Stats Data:")
            #self.debugLog(data)
            if type(salary) == str:
                data['fppgsal'] = (data['fppg']*1000)/float(salary)
            else:
                data['fppgsal'] = data['fppg']
            if salary != None:
                if restrictions(data)==True:
                    self.player_stats.append(data)
                    if position == "LW" or position == "RW":
                        self.wing_stats.append(data)
                    elif position == "C":
                        self.center_stats.append(data)
                    elif position == "D":
                        self.defence_stats.append(data)


#======================= Static Methods =======================
    @staticmethod
    def getOppTeams(sq3, team, date):
        oppteams = sq3.executeQueryDict("""SELECT hteamstr, vteamstr from
        boxscore where gamedate='"""+date+"""'
        and(vteamstr='"""+team+"""' or hteamstr='"""+team+"""')
        """)
        return oppteams
    @staticmethod
    def getDBPlayerData(sq3, playerName, season):
        player_data = sq3.executeQueryDict("""SELECT d.id, d.boxscore,
        d.team, b.vteamstr, b.hteamstr, d.player, d.shots, d.goals, d.assists, d.points,
        d.time_on_ice FROM boxscore_data d, boxscore b
        WHERE d.player='"""+playerName+"""' AND
        b.id=d.boxscore AND b.season='"""+season+"""';
        """)
        return player_data
    @staticmethod
    def getSeconds(myStr):
        minutes = int(myStr.split(':')[0])
        seconds = int(myStr.split(':')[1])
        return minutes*60+seconds
    @staticmethod
    def getTimeStr(seconds):
        myMin = int(seconds/60)
        mySec = seconds % 60
        return str(myMin)+':'+str(mySec)
    @staticmethod
    def getPlayerSalary(player, dkdata):
        for data in dkdata:
            if player == data['player']:
                return data['salary']
    @staticmethod
    def getPlayerPosition(player, dkdata):
        for data in dkdata:
            if player == data['player']:
                return data['position']
    @staticmethod
    def getDkpoints(goals, assists, shots, blocks, shp):
        dk_points = 0
        dk_points += goals * 3.0
        dk_points += assists * 2
        dk_points += shots * 0.5
        dk_points += blocks * 0.5
        dk_points += shp * 0.2
        if goals > 2:
            dk_points += 1.2
        return dk_points
    @staticmethod
    def getTodaysPlayersFromTeam(player_list, boxscores):
        todays_players = []
        for boxscore in boxscores:
            #print boxscore['vteamstr']+" VS "+boxscore['hteamstr']
            vteam_players = DKUtil.getPlayersFromTeam(player_list, boxscore['vteamstr'])
            hteam_players = DKUtil.getPlayersFromTeam(player_list, boxscore['hteamstr'])
            #print len(vteam_players)
            todays_players.extend(vteam_players)
            todays_players.extend(hteam_players)
        return todays_players
    @staticmethod
    def getPlayersFromTeam(player_list, teamstr):
        team_player_list = []
        for player in player_list:
            if player['team'] == teamstr:
                team_player_list.append({'player':player['player'],'team':player['team']})
        return team_player_list
    @staticmethod
    def getPlayerSummaryStats(player, team, player_data):
        player_stats = {}
        GP = 0
        goals = 0
        assists = 0
        points = 0
        shots = 0
        time_on_ice_s = 0
        blocks = 0
        shp = 0
        so_goals = 0
        dk_points = 0
        dk_points_per_min = 0
        dk_sd_sum = 0
        dk_sd = 0
        for data in player_data:
            GP += 1
            goals += data['goals']
            assists += data['assists']
            points += data['points']
            shots += data['shots']
            time_on_ice_s += DKUtil.getSeconds(data['time_on_ice'])
            temp_dk_points = DKUtil.getDkpoints(data['goals'], data['assists'], data['shots'], 0, 0)
            dk_points += temp_dk_points
            dk_sd_sum += temp_dk_points**2

        #player_stats['player'] = player_data['player']
        #player_stats['team'] = player_data['team']
        dk_sd = math.sqrt(dk_sd_sum/GP)
        time_on_ice_s = int(time_on_ice_s/GP)
        fppg = dk_points/GP
        player_stats['player'] = player
        player_stats['team'] = team
        player_stats['gp'] = GP
        player_stats['goals'] = goals
        player_stats['assists'] = assists
        player_stats['points'] = points
        player_stats['shots'] = shots
        player_stats['time_on_ice'] = DKUtil.getTimeStr(time_on_ice_s)
        player_stats['time_on_ice_s'] = time_on_ice_s
        player_stats['blocks'] = blocks
        player_stats['shp'] = shp
        player_stats['so_goals'] = so_goals
        player_stats['dk_points'] = dk_points
        player_stats['fppg'] = fppg
        player_stats['variance'] = dk_sd
        return player_stats
