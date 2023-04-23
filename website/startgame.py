from flask import Blueprint, render_template
import random

from . import db   ##means from __init__.py import db
from .models import gameStats


game = Blueprint('game',__name__)

@game.route('/startgame')
def home():
    display_messages = []
    # Define the deck of cards
    shapes = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King','Ace']
    deck = [(card, shape) for shape in shapes for card in cards]

    # Shuffle the deck
    random.shuffle(deck)

    # Split the deck into two halves
    half1 = deck[:26]
    half2 = deck[26:]

    # Define a function to play a round of War
    def play_round(player1, player2):
        player1_card = player1.pop(0)
        player2_card = player2.pop(0)
        display_messages.append(f'Player 1 plays {player1_card[0]} of {player1_card[1]}')
        display_messages.append(f'Player 2 plays {player2_card[0]} of {player2_card[1]}')

        if cards.index(player1_card[0]) > cards.index(player2_card[0]):
            display_messages.append('Player 1 wins the round!')
            player1.append(player1_card)
            player1.append(player2_card)

        elif cards.index(player2_card[0]) > cards.index(player1_card[0]):
            display_messages.append('Player 2 wins the round!')
            player2.append(player2_card)
            player2.append(player1_card)

        else:
            display_messages.append('War!')
            war_cards = [player1_card, player2_card]
            
            while True:
                if len(player1) < 2:
                    display_messages.append('Player 2 wins the war!')
                    player2.extend(war_cards + player1)
                    break
                elif len(player2) < 2:
                    display_messages.append('Player 1 wins the war!')
                    player1.extend(war_cards + player2)
                    break
                else:
                    player1_facedown = player1.pop(0)
                    player2_facedown = player2.pop(0)
                    player1_faceup = player1.pop(0)
                    player2_faceup = player2.pop(0)
                    
                    display_messages.append(f'Player 1 war card is {player1_faceup[0]} of {player1_faceup[1]}')
                    display_messages.append(f'Player 2 war card is {player2_faceup[0]} of {player2_faceup[1]}')

                    print(f'Player 1 war card is {player1_faceup[0]} of {player1_faceup[1]}')
                    print(f'Player 2 war card is {player2_faceup[0]} of {player2_faceup[1]}')
                    
                    if cards.index(player1_faceup[0]) > cards.index(player2_faceup[0]):
                        display_messages.append('Player 1 wins the round!')
                        player1.extend(war_cards)
                        player1.append(player1_faceup)
                        player1.append(player2_faceup)
                        player1.append(player1_facedown)
                        player1.append(player2_facedown)
                        break
                    
                    elif cards.index(player2_faceup[0]) > cards.index(player1_faceup[0]):
                        display_messages.append('Player 2 wins the round!')
                        player2.extend(war_cards)
                        player2.append(player2_faceup)
                        player2.append(player1_faceup)
                        player2.append(player2_facedown)
                        player2.append(player1_facedown)
                        break
                    
                    else:
                        war_cards.append(player1_facedown)
                        war_cards.append(player2_facedown)
                        war_cards.append(player1_faceup)
                        war_cards.append(player2_faceup)

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

