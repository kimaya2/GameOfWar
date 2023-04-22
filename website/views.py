from flask import Blueprint, render_template

from . import db   ##means from __init__.py import db
from .models import gameStats

views = Blueprint('views',__name__)

@views.route('/')
def home():
    return render_template('base.html')

@views.route('/playerstats',methods=['GET'])
def view_playerstats():
    user1 = gameStats.query.filter_by(name='Player 1').first()
    user2 = gameStats.query.filter_by(name='Player 2').first()

    if user1:
        return render_template('playerstats.html', player1=user1, player2=user2)
    else:
        return render_template('playerstats.html', message = 'No Games Played')