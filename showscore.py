#!/usr/bin/python3

from flask import Blueprint,render_template,request,redirect,make_response
#from werkzeug import secure_filename

from config import TEAMS
from database import getOwnSong, getSpecSong, getTeamSongTop, getSong, getOneSong, getScore, getOnePlayer, getPlayer, getNonSpecScore

Score = Blueprint('Score',__name__)

@Score.route('/')
def showTeams():
    return 'nothing'

@Score.route('/team/')
def showOwn():
    return 'nothing'

@Score.route('/team/<team>')
def showOwnScore(team):
    songList=getSong()

    teamInfo=[]
    teamInfo.append(team)
    teamInfo.append(TEAMS[int(team)-1][1])

    scoreList=[]
    for song in songList:
        scoreList.append(getTeamSongTop(team,song['SongID'],3))
    return render_template('score.html',TEAMS=TEAMS,songList=songList,scoreList=scoreList,teamInfo=teamInfo)

@Score.route('/team/<teamID>/song/<songid>')
def showTeamSongScore(teamID,songid):
    songList=getOneSong(songid)

    teamInfo=[]
    teamInfo.append(teamID)
    teamInfo.append(TEAMS[int(teamID)-1][1])

    scoreList=[]
    scoreList.append(getTeamSongTop(teamID,songid,10000))
    return render_template('score_team_detial.html',TEAMS=TEAMS,songList=songList,scoreList=scoreList,teamInfo=teamInfo)

@Score.route('/personal/')
def showRank():
    Players=getPlayer()
    for player in Players:
        player['TeamName'] = TEAMS[ player['TeamID'] -1 ][1]

    return render_template('score_personal_message.html',TEAMS=TEAMS,Players=Players)

@Score.route('/personal/<playerid>')
def showPlayerScore(playerid):
    playerInfo=[getOnePlayer(playerid)]
    playerInfo.append(TEAMS[playerInfo[0]['TeamID']-1][1])

    #Scores=getScore(playerid,0,10000)
    Scores=getNonSpecScore(playerid,0,10000)
    return render_template('score_personal.html',TEAMS=TEAMS,playerInfo=playerInfo,Scores=Scores)


