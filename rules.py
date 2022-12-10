from dataclasses import dataclass


@dataclass
class Rules:
    NUM_PLAYERS: int
    WIN_SCORE: int
    OPEN_CARDS_PER_LEVEL: int = 4 
    MAX_HAND_CARDS: int = 3
    MAX_PLAYER_GEMS: int = 10
    MAX_GEMS_TAKE: int = 3 
    MAX_SAME_GEMS_TAKE: int = 2
    MIN_SAME_GEMS_STACK: int = 4
    MAX_GOLD: int = 5

    def __post_init__(self):
        self.NOBLE_AMOUNT = self.NUM_PLAYERS + 1
        self.MAX_GEMS_IN_STACK = 7 if self.NUM_PLAYERS == 4 else 2 + self.NUM_PLAYERS
