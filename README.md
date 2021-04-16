# PySplendor
Splendor game in command line interface.

## Dependencies
- Written in Python 3.8
- Works with Python 3.7+
- No external libraries needed.

## How to Run
- Download/clone this repository and run [\_\_main\_\_.py](__main__.py) with Python.

## How to Play?
This game is based in Splendor. You can learn the actual rules of the game from [here.](https://www.ultraboardgames.com/splendor/game-rules.php)  
The differences with original game are:  
- Reserved cards aren't hidden.
- You can't choose a noble when there is more than one eligible noble deserved.
- In addition to the 15 point game option, there is also a 21 point game option.

Inside this command line game, you can perform 6 different actions: 
* take gems, reserve card, purchase card, purchase hand card, quit, see help.  

Whenever a prompt asks you to type an input, type one of these actions.

**tXXX**: Take a gem
- "X" are chars: 'r','g','b','w','k' (red, green, blue, white, black) which represents colors of gems
- You can enter from 0 to 3 characters after "t"
- Typing only "t" means 'pass'
- **EXAMPLE INPUT**: "trgb" means take red, green and blue
- **EXAMPLE INPUT**: "tww" means take two white gems
- **EXAMPLE INPUT**: "tb" means take one blue gem
    
**rXY**: Reserve a card
- "X" is digit from 1 to 3
- "Y" is digit from 0 to 3
- **EXAMPLE INPUT**: "r12" means from 1st level, reserve 2nd card 
- **EXAMPLE INPUT**: "r20" means from 2nd level, do a blind reserve
- You **MUST** enter **TWO** digits after "r"
    
**pXX**: Purchase a card
- "X" is digit from 1 to 3
- **EXAMPLE INPUT**: "p33" means from 3rd level, purchase 3rd card
- You **MUST** enter **TWO** numbers after "p"
    
**hX**: Purchase from Hand (from already reserved cards)
- "X" is digits from 1 to 3
- **EXAMPLE INPUT**: "h1" means purchase 1st card in your hand (the cards you already reserved)
- You **MUST** enter **ONE** number after "h"
    
**quit**: Quit game  
**help**: Show help text (you can see this help document inside game whenever you need) 

---

In addition to game related actions, you can type these options whenever a prompt comes (even right before the game when it says "press ENTER to start game"):  
- **emoji1**: Enable the emoji mode. Color emojis are shown instead of gem names "r, g, b, w, k". By default, emojis are enabled.  
- **emoji0**: Disable the emoji mode. Gems are shown by chars "r, g, b, w, k".  
- **sleep1**: AI thinking time is set to 0.2 seconds. Default option.  
- **sleep0**: AI thinking time is disabled. Practically it's 0 seconds. Although it's not recommended in order to follow the game, you can use this option for AI vs AI fights.

## Features
- A basic one-move-foreseeing AI, which is open for improving.
- Elo scoring system, which you may be familiar from chess, is used for players and account data is stored in Accounts folder.
