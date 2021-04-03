from dataclasses import dataclass
@dataclass(frozen=True)
class Rules:
    NUM_PLAYERS: int
    WIN_SCORE: int
    MAX_OPEN_CARDS = 4 
    MAX_HAND_CARDS = 3
    MAX_PLAYER_GEMS = 10
    MAX_GEMS_TAKE = 3 
    MAX_SAME_GEMS_TAKE = 2
    MIN_SAME_GEMS_STACK = 4
    MAX_GOLD = 5

    def __post_init__(self):
        object.__setattr__(self,"MAX_NOBLES", self.NUM_PLAYERS + 1)
        object.__setattr__(self,"MAX_GEMS", 7 if self.NUM_PLAYERS == 4 else 2 + self.NUM_PLAYERS)