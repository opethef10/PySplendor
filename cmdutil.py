"""Command line util for the PySplendor game.
Each action in the game is done by typing them to the command prompt
Parsed commands then do the actions and affects the game state
"""

from cmd import Cmd

from splendorgame import SplendorGame
from player import Player


class CmdUtil(Cmd):
    def __init__(self, human, ai, score, sleep):
        super().__init__()
        self.game = SplendorGame(human, ai, score)
        self.prompt = f"({self.game.currentPlayer.name}) "
        self.cmdqueue = self.game.currentPlayer.possible_moves(self.game)
        Player.sleepTime = sleep

    def onecmd(self, line):
        """Print value errors when an action failed therefore don't update the game state and re-prompt"""
        try:
            return super().onecmd(line)
        except ValueError as valueError:
            print("*** PySplendor:", valueError)

    def precmd(self, line):
        """For AI player give them some time to think"""
        self.game.currentPlayer.think(line)
        return line

    def postcmd(self, correct_input, line):
        """Print game state when an action is completed correctly. """
        """Change the move count and reset the possible moves for AI"""
        if correct_input:
            if self.game.check_win():
                print(self.game)
                return True
            self.game.move_to_next()
            print(self.game)
            self.prompt = f"({self.game.currentPlayer.name}) "
            self.cmdqueue = self.game.currentPlayer.possible_moves(self.game)

    def preloop(self):
        """Before the start of the game"""
        print(self.game)

    def postloop(self):
        """After the game is completed"""
        if self.game.check_win():
            self.game.update_elo()
            self.game.print_results()

    def emptyline(self):
        """Ignore when an empty prompt is sent"""

    def do_exit(self, _):
        """Exit the game"""
        raise SystemExit()

    do_quit = do_EOF = do_exit

    def do_print(self, _):
        """Print the current game state"""
        print(self.game)

    def do_take(self, action_string):
        """Usage: take XXX
        "X" are chars: 'r','g','b','w','k' (red, green, blue, white, black) which represents colors of gems
        EXAMPLE INPUT: "take rgb" means take red, green and blue
        EXAMPLE INPUT: "take ww" means take two white gems
        EXAMPLE INPUT: "take b" means take one blue gem
        You can enter from 0 to 3 characters after "take"
        Typing only "take" means 'pass'
        """
    
        gem_lst = list(action_string)
        self.game.currentPlayer.take_gems(self.game, gem_lst)
        return True

    def do_reserve(self, action_string):
        """Usage: reserve XY
        "X" is digit from 1 to 3
        "Y" is digit from 0 to 3
        EXAMPLE INPUT: "reserve 12" means from 1st level, reserve 2nd card 
        EXAMPLE INPUT: "reserve 20" means from 2nd level, do a blind reserve
        You MUST enter TWO digits after "reserve" command!
        """
        level = int(action_string[0]) - 1
        pos = int(action_string[1]) - 1
        self.game.currentPlayer.reserve(self.game, level, pos)
        return True

    def do_purchase(self, action_string):
        """Usage: purchase XY
        "X" is digit from 0 to 3
        "Y" is digit from 1 to 3
        If X is 0, it means you purchase from your reserved cards, otherwise it refers to card levels
        EXAMPLE INPUT: "purchase 32" means from 3rd level, purchase 2nd card
        EXAMPLE INPUT: "purchase 01" means from your reserved cards, purchase 1st card
        You MUST enter TWO numbers after "purchase" command!
        """
        level = int(action_string[0]) - 1
        pos = int(action_string[1]) - 1
        if level == -1:
            level = None
        self.game.currentPlayer.purchase(self.game, level, pos)
        return True

    def do_sleep(self, line):
        """Usage: sleep X'
        Set AI sleep time between X seconds. X can be only between [0.0, 0.5]
        If no numbers given, prints current AI sleep setting
        """
        if not line:
            print(f"*** PySplendor: Current AI sleep time is {Player.sleepTime} seconds")
        else:
            duration = float(line)
            if not 0 <= duration <= 0.5:
                raise ValueError("Sleep duration should be between 0 and 0.5 second")
            Player.sleepTime = duration
            print(f"*** PySplendor: AI sleep time is set to {duration} seconds")
