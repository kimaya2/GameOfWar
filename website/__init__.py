from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "gameDatabase.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hdsbdhfudsfuiewunifjfnkj'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_NAME
    db.init_app(app)

    from .views import views
    from .startgame import game

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(game,url_prefix='/')

    with app.app_context():
        db.create_all()

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')