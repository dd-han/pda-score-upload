# Project Diva Arcade 成績上傳系統

## 起源

因為當了別人比賽的委員，同時有接觸到Python + Flask，發現專題不想用php寫了（蛤），但是需要一個小專案來練習Python + Flask的寫法，所以就跑去問對方「須不需要一個成績圖上傳系統？」

於是這東西就出現了。

## 系統需求

* Python3
* Flask
* Flask-Social
* Facebook API

## 安裝步驟

    pacman -S python3
    wget https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py
    python3 -m pip install Flask
    python3 -m pip install Flask-Social
    python3 -m pip install Flask-SQLAlchemy
    python3 -m pip install https://github.com/sbook/flask-mongoengine/tarball/master
    python3 -m pip install http://github.com/pythonforfacebook/facebook-sdk/tarball/master

