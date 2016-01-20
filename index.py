from flask import request , render_template , Blueprint, url_for , redirect


main = Blueprint('main',__name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    return "index!!!!!!"
