#!/usr/bin/python3

from flask import Blueprint,render_template,request,redirect,make_response
#from werkzeug import secure_filename

from config import TEAMS
from database import getOwnSong, getSpecSong, getTeamSongTop, getSong

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
    scoreList=[]
    for song in songList:
        scoreList.append(getTeamSongTop(team,song['SongID'],3))
    return render_template('score_team.html',TEAMS=TEAMS,teamname=TEAMS[int(team)-1][1],songList=songList,scoreList=scoreList)

@Score.route('/personal/')
def showRank():
    return render_template('score_personal.html')

@Score.route('/personal/<playerid>')
def showPlayerScore(team):
    songList=getSong()
    scoreList=[]
    for song in songList:
        scoreList.append(getTeamSongTop(team,song['SongID'],3))
    return render_template('score_team.html',TEAMS=TEAMS,teamname=TEAMS[int(team)-1][1],songList=songList,scoreList=scoreList)


