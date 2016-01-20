#!/usr/bin/python3

import os
import hashlib
import random 
import shutil
from flask import Blueprint,render_template,request,redirect,make_response
#from werkzeug import secure_filename

import facebook
from config import SERVER_WITH_HTTPS

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
    if request.method == 'POST':
        file = request.files['image']
        if file and allowed_file(file.filename):
            try:
                ## 整理資訊
                fbToken=request.cookies.get('fbToken')
                player=facebook.getName(fbToken)
                song = request.form.get('song')
                remeber = request.form.get('remeber',False)
                #song = request.form['song'];
                #remeber = request.form['remeber'];
                fileExt = '.'+getExt(file.filename)

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
                folder = os.path.join(UPLOAD_FOLDER, player)
            except:
                return "發生錯誤"

            if not os.path.exists(folder):
                os.makedirs(folder)

            fullpath = os.path.join(folder,song+fileExt)
            shutil.copy2(temp_fullpath,fullpath)
            
            os.remove(temp_fullpath)

            return "upload Sucesfull file tempory as " + temp_filename + " md5 is " + hasher.hexdigest() + " and Player is " + player

        else:
            return '檔案格式不被許可！！'
    else:
        code = request.args.get('code',False)
        if code:
            Res=facebook.getToken(request.base_url,code)
            if Res[0]:
                resp = make_response(redirect(request.base_url))
                #resp = make_response("寫入Cookie中......"+Res[1]+Res[2])
                resp.set_cookie(key='fbToken',value=Res[1],max_age=int(Res[2]),secure=SERVER_WITH_HTTPS)
                return resp
                
            else:
                return "登入失敗，請重試，錯誤訊息："+Res[1]
            
        else:
            if request.cookies.get('fbToken'):
                fbToken=request.cookies.get('fbToken')
                fbid=facebook.getName(fbToken)
                #fbid='登入成功'
            else:
                LoginURL=facebook.genGetCodeURL(request.base_url)
                fbid='您尚未登入，<a href=\"'+LoginURL+'\">使用facebook登入</a>'

            return render_template('upload.html',fbid=fbid)
