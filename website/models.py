from . import db

class gameStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000))
    num_of_games = db.Column(db.Integer, default=0)
    num_of_wins = db.Column(db.Integer, default = 0)
