from SplendorGame import SplendorGame

#--------------- CREATE GAME ---------------#

while True: #check for invalid inputs
    try:
        total=int(input("How many players are there in this game? (type 2, 3 or 4): "))
        assert total in (2,3,4)
        break
    except (AssertionError,ValueError):
        print(f"Invalid input! Try again\n")
        
while True: #check for invalid inputs 
    try:
        ai=int(input(f"How many of them are AI: (type {str(tuple(range(total+1)))[1:-4]} or {total}): "))
        assert 0<=ai<=total
        human=total-ai
        break
    except (AssertionError,ValueError):
        print(f"Invalid input! Try again\n")        
        
while True: #check for invalid inputs 
    try:
        winScore=int(input("What is win score? (type 15 or 21): "))
        assert winScore in (15,21)
        break
    except (AssertionError,ValueError):
        print(f"Invalid input! Try again\n")

game=SplendorGame(human,ai,winScore) #construct a Splendor game, rules will differ depending on total number of players
game.start()

#----------------- GAME LOOP -----------------#

while not game.checkWin(): #play until someone wins
    for player in game.players:   
        print(game) #print current state of the game
        moveSet = player.possibleMoves(game) #move set for AI
        while True: # check for invalid action inputs
            try:
                actionString=player.getInput(moveSet) #for human, enter input; for AI, it will return the string of the best move from moveSet
                game.doAction(player,actionString)
                break
            except AttributeError as err:
                print(err)

print(game)
game.printResults()