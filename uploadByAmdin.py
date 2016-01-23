#!/usr/bin/python3

import os
import hashlib
import random 
import shutil
from flask import Blueprint,render_template,request,redirect,make_response
#from werkzeug import secure_filename

import facebook
from config import SERVER_WITH_HTTPS , TEAMS

from database import lookupAdmin, getSong, insScoreAdmin, getPlayer

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = set(['jpg','png','jpeg'])

Uploader = Blueprint('Uploader',__name__)

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def getExt(filename):
    return '.' in filename and filename.rsplit('.',1)[1]

@Uploader.route('/', methods=['GET','POST'])
def upload():
    ## POST
    if request.method == 'POST':
        file = request.files['image']
        if not facebook.getUID(request.cookies.get('fbToken')):
            return "session已過期"

        elif not lookupAdmin(facebook.getUID(request.cookies.get('fbToken'))):
            return "您不是管理員，滾！！"

        elif not request.form.get('song'):
            return "您沒有選擇歌曲！！"

        elif not request.form.get('Rate'):
            return "您沒有輸入達成率！！"

        elif not request.form.get('PlayerID'):
            return "您沒有選擇玩家！！"

        elif not file:
            return "你沒有選擇檔案！！"

        elif not allowed_file(file.filename):
            return "檔案格式錯誤！！"

        else:
            try:
                ## 整理資訊
                song    = request.form.get('song')
                rate    = request.form.get('Rate')
                PlayerID= request.form.get('PlayerID')
                fileExt = '.'+getExt(file.filename)
                ## 未來再實做的功能
                #remeber = request.form.get('remeber',False)

            except:
               return render_template('upload_msg.html',TEAMS=config.TEAMS,message="欄位輸入不完整")

            try:
                ## 產生暫存的檔名
                temp_filename = "temp-"+str(random.randint(1,10000))+fileExt
                temp_fullpath = os.path.join(UPLOAD_FOLDER, temp_filename)
                file.save(temp_fullpath)
            
                ## 歸位--動態網頁用
    
                ## 產生sha1
                BLOCKSIZE = 65536
                hasher = hashlib.sha1()
                with open(temp_fullpath,'rb') as afile:
                    buf = afile.read(BLOCKSIZE)
                    while len(buf) > 0:
                        hasher.update(buf)
                        buf = afile.read(BLOCKSIZE)
                sha1=hasher.hexdigest()
                
                fullpath = os.path.join(UPLOAD_FOLDER,sha1+fileExt)
                shutil.copy2(temp_fullpath,fullpath)

                ## 歸位--靜態網頁用
                folder = os.path.join(UPLOAD_FOLDER, 'player-'+str(PlayerID))
                if not os.path.exists(folder) :
                    os.makedirs(folder)

                fullpath = os.path.join(folder,'song-'+song+fileExt)
                shutil.copy2(temp_fullpath,fullpath)
                
                ## 刪除暫存檔案
                os.remove(temp_fullpath)

            except:
                return render_template('upload_msg.html',message="存檔有問題，可能硬碟滿了，請通知管理員。")

               # return "upload Sucesfull file tempory as " + temp_filename +\
               #     " md5 is " + hasher.hexdigest() + " and Player is " + player

            try:
                insScoreAdmin(PlayerID,song,sha1,fileExt,rate,facebook.getUID(request.cookies.get('fbToken')))

            except:
                return render_template('upload_msg.html',message="資料庫有點毛病")

            return render_template('upload_msg.html',message="存檔成功")

    ## GET METHOD
    else:
        code = request.args.get('code',False)
        if code:
            Res=facebook.getToken(request.base_url,code)
            if Res[0]:
                AdminUID=facebook.getUID(Res[1])
                AdminInfo=lookupAdmin(AdminUID)
                if AdminInfo:
                    resp = make_response(redirect(request.base_url))
                    #resp = make_response("寫入Cookie中......"+PlayerUID+PlayerInfo['CardName'])
                    resp.set_cookie(key='fbToken',value=Res[1],max_age=int(Res[2]),\
                            secure=SERVER_WITH_HTTPS)
                    resp.set_cookie(key='AdminName',value=AdminInfo['AdminName'],max_age=int(Res[2]),\
                            secure=SERVER_WITH_HTTPS)
                    return resp

                else:
                    return render_template('upload_msg.html',message="您似乎不是管理員，如果有什麼誤會請回報你的FacenookID："+AdminUID)
                
            else:
                return render_template('upload_msg.html',message="登入失敗，請重試，錯誤訊息："+Res[1])
            
        else:
            if request.cookies.get('fbToken'):
                fbToken=request.cookies.get('fbToken')
                AdminName=request.cookies.get('AdminName')
                
                if lookupAdmin(facebook.getUID(fbToken)):
                    songinfo = getSong()
                    playerinfo = getPlayer()
                    return render_template('upload_by_admin.html',TEAMS=TEAMS,AdminName=AdminName,songs=songinfo,players=playerinfo)
                else:
                    if not facebook.getUID(fbToken):
                        return render_template('upload_msg.html',\
                                message='Token過期，請重新登入：'+"<a href=\""+facebook.genGetCodeURL(request.base_url)+"\">使用facebook登入</a>")
                    else:
                        return render_template('upload_msg.html',message='你以為產生Token送給我，我就會吃嘛！！')

            else:
                LoginURL=facebook.genGetCodeURL(request.base_url)
                msg='您尚未登入，<a href=\"'+LoginURL+'\">使用facebook登入</a>'
                return render_template('upload_msg.html',message=msg)

