from flask import request , render_template , Blueprint, url_for , redirect

from config import TEAMS
from database import getMember

main = Blueprint('main',__name__)

@main.route('/')
def showIndex():
    
    teamList = []
    for team in TEAMS:
        teaminfo = getMember(team[0])
        teamList.append( [team,teaminfo] );

    return render_template('index.html',TEAMS=TEAMS,TEAMSMEMBER=teamList)
