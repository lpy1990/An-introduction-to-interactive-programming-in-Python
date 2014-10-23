# implementation of card game - Memory

import simplegui
import random

CARD_WIDTH = 50
CARD_LENGTH = 100



# helper function to initialize globals
def new_game():
    global state,counter,posion
    global cards,position,exposed
    exposed = []
    position = []
    cards = []
    state = 0
    counter = 0
    for i in range(16):
        if i < 8:
            cards.append(i)
            position.append(i*50)
            exposed.append(False)
        else:
            cards.append(i-8)
            position.append(i*50)
            exposed.append(False)
    random.shuffle(cards)
    label.set_text('Tunes =' + str(counter))
            

#    print cards,type(cards),position,type(position) 

     
# define event handlers

def mouseclick(pos):
    global cards,exposed,state,first_card,second_card,choice_1,choice_2,counter
    k = pos[0]//50
    if exposed[k] == False:

        if state == 0:
            exposed[k] = True
            choice_1= k
            first_card = cards[k]
            counter += 1
            state = 1
        
        
        
        elif state == 1:
            exposed[k] = True
            choice_2 = k
            second_card = cards[k]                               
            state = 2
        else:
        
            if first_card != second_card:
            
                exposed[choice_1] = False
                exposed[choice_2] = False
            
            
            exposed[k] = True
            choice_1= k
            first_card = cards[k]
            counter += 1        	
            state = 1 
    label.set_text('Tunes =' + str(counter))
#    print counter
            
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(16):
        if exposed[i] == True :
            canvas.draw_text(str(cards[i]), [position[i]+15 , CARD_LENGTH//1.5], 50, "Red")
        elif exposed[i] == False:
            canvas.draw_line((position[i]+CARD_WIDTH//2, 0), (position[i] + CARD_WIDTH//2, CARD_LENGTH), CARD_WIDTH-1, 'Green')
        
            

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Tunes = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
