# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome1 = ""
outcome2 = ""
score = 0
win = 0
lose = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand =[]

    def __str__(self):
       # return a string representation of a hand
        ans = ""
        for i in range(len(self.hand)):
            ans += str(self.hand[i])+" "
        return "Hand contains"+ ans
        
    def add_card(self, card):
       # add a card object to a hand
        self.hand.append(card)

    def get_value(self):
        get_ace = False
        value = 0		
        for card in self.hand:
            
            if card.get_rank() == "A":
                get_ace = True
            
            value += VALUES[card.get_rank()]
            
        if get_ace and value <= 11:
            value += 10                                
        return value                    
# define deck class 
class Deck:
    def __init__(self):
        self.choice = 52
        self.deck_list = []
        
        for i in SUITS:
            for j in RANKS:
                new_card = Card(i, j)
                self.deck_list.append(new_card)
        
                

    def shuffle(self):
        # shuffle the deck 	
        random.shuffle(self.deck_list)
    def deal_card(self):                       
        
        return self.deck_list.pop()
    
    def __str__(self):
        ans = ""
        for i in range(len(self.deck_list)):
            ans += str(self.deck_list[i])+" "
        return "Deck contains"+ans        

#define event handlers for buttons
def deal():
    global outcome1,outcome2, in_play,deck,player_hand,dealer_hand,win,lose
    
    if in_play:
        outcome2 = "You forfeited game! You Lose!"
        outcome1 = "New deal?"
        win += 1
        in_play = False
    else:
        
        deck = Deck()
        deck.shuffle()
        player_hand = Hand()
        dealer_hand = Hand()
    
        player_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())    
        outcome1 = "Hit or Stand?"
        outcome2 = ""
        in_play = True

def hit():
    global outcome1,outcome2, in_play,player_hand,deck,win,lose
    if in_play:
        player_hand.add_card(deck.deal_card())
        
        if player_hand.get_value()> 21:                       
            outcome2 = "You are busted"
            win += 1
            in_play = False
            outcome1 = "New deal?"
    
def stand():
    global outcome1,outcome2,in_play,player_hand,win,lose
    
    if in_play:
        
        while dealer_hand.get_value()< 17:
            dealer_hand.add_card(deck.deal_card())
            
        if dealer_hand.get_value()>21:
            outcome2 = "dealer busted"
            lose += 1
           
            in_play = False
            
        else:
            if player_hand.get_value() > dealer_hand.get_value():
                outcome2 = "You Win!"
                lose += 1
                in_play = False
            else:
                outcome2 = "You Lose!"
                win += 1
                in_play = False
        outcome1 = "New deal?"             
                
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    canvas.draw_text('Black Jack', (200, 50), 50, 'Yellow')
    canvas.draw_text('Dealer:', (10, 120), 30, 'Yellow')
    canvas.draw_text('Player:'+str(player_hand.get_value()), (10, 290), 30, 'Yellow')
    canvas.draw_text(outcome2, (200, 500), 30, 'White')
    canvas.draw_text(outcome1, (200, 550), 30, 'White')
    canvas.draw_text("Dealer Wins:"+ str(win), (200, 120), 20, 'White')
    canvas.draw_text("Dealer Losses:"+ str(lose), (400, 120), 20, 'White')
    canvas.draw_text("Player Wins:"+ str(lose), (200, 290), 20, 'White')
    canvas.draw_text("Player Losses:"+ str(win), (400, 290), 20, 'White')
    player_pos = [10,320]
    dealer_pos = [10,150]
    for card in player_hand.hand:
        card.draw(canvas, player_pos)
        player_pos[0] += 1.2*CARD_SIZE[0]
    for card in dealer_hand.hand:
        card.draw(canvas, dealer_pos)
        dealer_pos[0] += 1.2*CARD_SIZE[0] 
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_SIZE, (46,198), CARD_SIZE)
    else:
        canvas.draw_text(str(dealer_hand.get_value()), (100, 120), 30, 'Yellow')
        

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
