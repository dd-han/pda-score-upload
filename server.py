#!/usr/bin/python3

from flask import Flask,render_template,request,redirect,url_for
from werkzeug.contrib.fixers import ProxyFix
import config

import index , upload

ScoreServer = Flask(__name__)

ScoreServer.register_blueprint(index.main)
ScoreServer.register_blueprint(upload.Uploader, url_prefix="/upload")
ScoreServer.secret_key=config.SERVER_SECURE_KEY
ScoreServer.wsgi_app = ProxyFix(ScoreServer.wsgi_app)


@ScoreServer.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

if __name__ == "__main__":
    ScoreServer.run(
            host=config.SERVER_HOST,
            port=config.SERVER_PORT,
            debug=config.SERVER_DEBUG)

