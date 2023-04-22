from flask import Blueprint, render_template
import random

from . import db   ##means from __init__.py import db
from .models import gameStats


game = Blueprint('game',__name__)

@game.route('/startgame',methods =['GET','POST'])
def home():
    display_messages = []
    # Define the deck of cards
    suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    deck = [(rank, suit) for suit in suits for rank in ranks]

    # Shuffle the deck
    random.shuffle(deck)

    # Split the deck into two halves
    half1 = deck[:26]
    half2 = deck[26:]

    # Define a function to play a round of War
    def play_round(player1, player2):
        card1 = player1.pop(0)
        card2 = player2.pop(0)
        display_messages.append(f'Player 1 plays {card1[0]} of {card1[1]}')
        display_messages.append(f'Player 2 plays {card2[0]} of {card2[1]}')
        if ranks.index(card1[0]) > ranks.index(card2[0]):
            display_messages.append('Player 1 wins the round!')
            player1.append(card1)
            player1.append(card2)
        elif ranks.index(card2[0]) > ranks.index(card1[0]):
            display_messages.append('Player 2 wins the round!')
            player2.append(card2)
            player2.append(card1)
        else:
            display_messages.append('Tie!')
            war_cards = [card1, card2]
            while True:
                if len(player1) < 4:
                    display_messages.append('Player 2 wins the war!')
                    player2.extend(war_cards + player1)
                    break
                elif len(player2) < 4:
                    display_messages.append('Player 1 wins the war!')
                    player1.extend(war_cards + player2)
                    break
                else:
                    display_messages.append('War!')
                    war_cards.extend(player1[:4])
                    war_cards.extend(player2[:4])
                    del player1[:4]
                    del player2[:4]

    # Play the game
    round_num = 1
    while len(half1) > 0 and len(half2) > 0:
        display_messages.append(f'Round {round_num}:')
        play_round(half1, half2)
        round_num += 1

    # Determine the winner
    if len(half1) > len(half2):
        display_messages.append('Player 1 wins the game!')
        winner = 'Player 1'
        loser = 'Player 2'
    elif len(half2) > len(half1):
        display_messages.append('Player 2 wins the game!')
        winner = 'Player 2' 
        loser = 'Player 1'       
    else:
        display_messages.append('The game ends in a tie!')

    user1 = gameStats.query.filter_by(name=winner).first()

    if user1:
        user1.num_of_games +=1
        user1.num_of_wins +=1
        db.session.commit()
    else:
        new_user = gameStats(name=winner, num_of_games=1, num_of_wins=1)
        db.session.add(new_user)
        db.session.commit()
    user2 = gameStats.query.filter_by(name=loser).first()

    if user2:
        user2.num_of_games +=1
        db.session.commit()
    else:
        new_user = gameStats(name=loser, num_of_games=1, num_of_wins=0)
        db.session.add(new_user)
        db.session.commit()

    return render_template('startgame.html', winner=winner,messages = display_messages)

