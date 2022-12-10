"""Command line util for the PySplendor game.
Each action in the game is done by typing them to the command prompt
Parsed commands then do the actions and affects the game state
"""

from cmd import Cmd
from pathlib import Path

from splendorgame import SplendorGame
from gemdict import GemDict
from player import Player

HELP_PATH = Path(__file__).with_name("help.txt")
PROMPT = "(Splendor) "


class CmdUtil(Cmd):
    def __init__(self, human, ai, score, emoji_flag, sleep):
        super().__init__()
        self.prompt = PROMPT
        self.game = SplendorGame(human, ai, score)
        self.HELP_STR = HELP_PATH.read_text()
        self.cmdqueue = self.game.currentPlayer.possible_moves(self.game)
        GemDict.emoji = emoji_flag
        Player.sleepTime = sleep

    def onecmd(self, line):
        """Print value errors when an action failed therefore don't update the game state and re-prompt"""
        try:
            return super().onecmd(line)
        except ValueError as valueError:
            print("valueError:", valueError)

    def precmd(self, line):
        """For AI player give them some time to think"""
        self.game.currentPlayer.think(line)
        return line

    def postcmd(self, correct_input, line):
        """Print game state when an action is completed correctly. """
        """Change the move count and reset the possible moves for AI"""
        if correct_input:
            print(self.game)
            if self.game.check_win():
                return True
            self.game.move_to_next()
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

    def do_help(self, _):
        print(self.HELP_STR)

    def do_exit(self, _):
        raise SystemExit()

    do_quit = do_EOF = do_exit

    def do_print_game(self, _):
        print(self.game)

    def do_take(self, action_string):
        """Parse action string and do the 'take' action for the current player"""
        gem_lst = list(action_string)
        self.game.currentPlayer.take_gems(self.game, gem_lst)
        return True

    def do_reserve(self, action_string):
        """Parse action string and do the 'reserve' action for the current player"""
        level = int(action_string[0]) - 1
        pos = int(action_string[1]) - 1
        self.game.currentPlayer.reserve(self.game, level, pos)
        return True

    def do_purchase(self, action_string):
        """Parse action string and do the 'purchase' action for the current player"""
        level = int(action_string[0]) - 1
        pos = int(action_string[1]) - 1
        self.game.currentPlayer.purchase(self.game, level, pos)
        return True

    def do_hand(self, action_string):
        """Parse action string and do the 'hand' action for the current player"""
        pos = int(action_string[0]) - 1
        self.game.currentPlayer.purchase(self.game, None, pos)
        return True

    def do_sleep(self, line):
        """Adjust the sleep time for AI"""
        if not line:
            print("Current sleep setting:", Player.sleepTime)
        else:
            duration = float(line)
            if not 0 <= duration <= 0.5:
                raise ValueError("Sleep duration should be between 0 and 0.5 second")
            Player.sleepTime = duration
            print(f"AI sleep time is set to {duration} seconds")

    def do_emoji(self, line):
        """Toggle the emoji setting for gems"""
        if not line:
            print("Current emoji setting:", GemDict.emoji)
        else:
            flag = bool(int(line))
            GemDict.emoji = flag
            print("Gem emojis are", "enabled" if flag else "disabled")
