create table boxscore (
id INTEGER primary key AUTOINCREMENT,
gamedate varchar(80),
hteamstr varchar(5),
vteamstr varchar(5),
link varchar(1000),
isparsed varchar(5)
);

alter table boxscore add season varchar(10);

create table boxscore_data (
id INTEGER primary key AUTOINCREMENT,
boxscore INTEGER,
team varchar(100),
ranker INTEGER,
player varchar(255),
goals INTEGER,
assists INTEGER,
points INTEGER,
plus_minus INTEGER,
pen_min INTEGER,
goals_ev INTEGER,
goals_pp INTEGER,
goals_sh INTEGER,
goals_gw INTEGER,
assists_ev INTEGER,
assists_pp INTEGER,
assists_sh INTEGER,
shots INTEGER,
shot_pct varchar(5),
shifts INTEGER,
time_on_ice varchar(10)
);

UPDATE boxscore SET isparsed='no' WHERE isparsed='yes';

SELECT id, gamedate, hteamstr, vteamstr FROM boxscore WHERE isparsed='yes'
SELECT d.id, d.boxscore, d.team, b.hteamstr, b.vteamstr, d.player, d.shots, d.goals, d.assists, d.points, d.time_on_ice FROM boxscore_data d, boxscore b WHERE d.player='Pavel Datsyuk' AND b.id=d.boxscore
SELECT distinct player from boxscore_data
SELECT distinct d.player, d.team from boxscore_data d, boxscore b WHERE d.boxscore = b.id AND b.season='2016';
SELECT id, vteamstr, hteamstr from boxscore where gamedate='2015-10-26';
SELECT count(d.id) as "GP", sum(d.goals) as "goals", sum(d.assists) as "assists", sum(d.points) as "points" from boxscore_data d, boxscore b where d.player='Andrew Cogliano' AND d.boxscore=b.id AND b.season='2016';
SELECT d.id, d.boxscore, d.team, d.player, d.shots, d.goals, d.assists, d.points, d.time_on_ice FROM boxscore_data d, boxscore b WHERE d.player='Pavel Datsyuk' AND b.id=d.boxscore AND b.season='2016';
