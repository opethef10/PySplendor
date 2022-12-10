import csv
from dataclasses import dataclass
from pathlib import Path
from random import shuffle

from gemdict import GemDict, ALL_GEMS, COLORED_GEMS, COLORS

cardsCsvPath = Path(__file__).with_name("cards.csv")


@dataclass(frozen=True)
class Card:
    color: str = None
    points: int = None
    price: GemDict = None
        
    def __str__(self):
        def map_color(gem):
            return COLORS[ALL_GEMS.index(gem)] if self.price.emoji else gem
        if self.color is None:
            return "[ ]"
        return f'[{map_color(self.color)} {self.points}|{self.price}]'

    @classmethod
    def get_cards(cls, max_open_cards):
        card_matrix = [[], [], []]
        with open(cardsCsvPath) as csvFile:
            next(csvFile)  # skip header
            for line in csv.reader(csvFile):
                assert len(line) == 8
                level = int(line[0]) - 1
                color = line[1]
                points = int(line[2])
                price = GemDict()
                for gem, amount in zip(COLORED_GEMS, line[3:]):
                    price.update(gem*int(amount))
                card = cls(color, points, price)
                card_matrix[level].append(card)
        
        for level in range(3):
            shuffle(card_matrix[level])
        
        decks = [level[:-max_open_cards] for level in card_matrix]
        open_cards = [level[-max_open_cards:] for level in card_matrix]
        return decks, open_cards
