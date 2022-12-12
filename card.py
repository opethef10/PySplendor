import csv
from dataclasses import dataclass
from pathlib import Path
from random import shuffle

from gemdict import GemDict, COLORED_GEMS

cardsCsvPath = Path(__file__).with_name("cards.csv")


@dataclass(frozen=True)
class Card:
    color: str = None
    points: int = None
    price: GemDict = None
    shape = "▮"
        
    def __str__(self):
        if self.color is None:
            return ""
        return f' {GemDict.map_color(self.color, self.shape):^6}  {self.points:^7} {self.price}'

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
                    if int(amount):
                        price.update({gem: int(amount)})
                card = cls(color, points, price)
                card_matrix[level].append(card)
        
        for level in range(3):
            shuffle(card_matrix[level])
        
        decks = [level[:-max_open_cards] for level in card_matrix]
        open_cards = [level[-max_open_cards:] for level in card_matrix]
        return decks, open_cards
