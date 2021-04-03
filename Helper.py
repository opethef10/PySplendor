HELP_STR="""\
HOW TO PLAY?
You can perform 6 different actions: take gems, reserve card, purchase card, purchase hand card, quit, see help

'tXXX': take gem
    "X" are chars: 'r','g','b','w','k' (red, green, blue, white, black) which represents colors of gems
    EXAMPLE INPUT: "trgb" means take red, green and blue
    EXAMPLE INPUT: "tww" means take two white gems
    EXAMPLE INPUT: "tb" means take one blue gem
    You can enter from 0 to 3 characters after "t"
    Typing only "t" means 'pass'
    
'rXY': reserve
    "X" is digit from 1 to 3
    "Y" is digit from 0 to 3
    EXAMPLE INPUT: "r12" means from 1st level, reserve 2nd card 
    EXAMPLE INPUT: "r20" means from 2nd level, do a blind reserve
    You MUST enter TWO digits after "r"
    
'pXX': purchase
    "X" is digit from 1 to 3
    EXAMPLE INPUT: "p33" means from 3rd level, purchase 3rd card
    You MUST enter TWO numbers after "p"
    
'hX': purchase from hand
    "X" is digits from 1 to 3
    EXAMPLE INPUT: "h1" means purchase 1st card in your hand (the cards you already reserved)
    You MUST enter ONE number after "h"
    
'quit': quit game
'help': show help text (you can see this document whenever you need) 
"""
