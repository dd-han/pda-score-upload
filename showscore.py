#!/usr/bin/python3

from flask import Blueprint,render_template,request,redirect,make_response
#from werkzeug import secure_filename

from config import TEAMS
from database import getOwnSong, getSpecSong, getTeamSongTop, getSong, getOneSong, getScore, getOnePlayer, getPlayer, getNonSpecScore, getSongTop, getSongScores

Score = Blueprint('Score',__name__)

def getUniqPlayerScore(score,count):
    uniqSongScore=[]
    playerList=[]
    count = 0
    for record in score :
        try:
            playerList.index(record['FBID'])
        except:
            playerList.append(record['FBID'])
            record['Count']=count+1
            uniqSongScore.append(record)
            count+=1
        if count > count:
            break

    return uniqSongScore

@Score.route('/team/<team>')
def showOwnScore(team):
    songList=getSong()

    teamInfo=[]
    teamInfo.append(team)
    teamInfo.append(TEAMS[int(team)-1][1])

    scoreList=[]
    for song in songList:
        songScore=getTeamSongTop(team,song['SongID'],10000)
        uniqSongScore = getUniqPlayerScore(score=songScore,count=3)
        scoreList.append( uniqSongScore )
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

@Score.route('/song')
def showSongRank():
    songList=getOwnSong()

    scoreList=[]
    for song in songList:
        songScore=getSongTop(song['SongID'],10000)
        uniqSongScore = getUniqPlayerScore(score=songScore,count=6)
        scoreList.append( uniqSongScore )
    #return render_template('score.html',TEAMS=TEAMS,songList=songList,scoreList=scoreList,teamInfo=teamInfo)
    return render_template('score_song.html',TEAMS=TEAMS,songList=songList,scoreList=scoreList)

@Score.route('/song/<songID>')
def showSongAllScore(songID):
    songList=[]
    songList.append(getOneSong(songID))

    scoreList=[]
    for song in songList:
        songScore=getSongScores(song['SongID'],10000)
        scoreList.append( songScore )
    #return render_template('score.html',TEAMS=TEAMS,songList=songList,scoreList=scoreList,teamInfo=teamInfo)
    return render_template('score_song_all.html',TEAMS=TEAMS,songList=songList,scoreList=scoreList)
