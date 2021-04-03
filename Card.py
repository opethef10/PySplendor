from GemDict import GemDict,GEMS,COLORS
from random import shuffle
from dataclasses import dataclass
import csv,os

splendorMainDir=os.path.dirname(__file__)
@dataclass(frozen=True)
class Card:
    color: str = None
    points: int = None
    price: GemDict = None
        
    def __str__(self):
        def mapColor(gem):
            return COLORS[GEMS.index(gem)] if self.price._emoji else gem
        if self.color is None:
            return "[ ]"
        return f'[{mapColor(self.color)} {self.points}|{self.price}]'

    @classmethod
    def getCards(cls,MAX_OPEN_CARDS):
        filepath = os.path.join(splendorMainDir, "cards.csv")
        CARDS = [[], [], []]
        with open(filepath) as csvFile:
            reader = csv.reader(csvFile)
            next(reader, None) # skip header
            for line in reader:
                assert len(line) == 8
                level = int(line[0]) - 1
                color = line[1]
                points = int(line[2])
                price=GemDict()
                for gem, amount in zip(GEMS[:-1], line[3:]):
                    if len(amount) == 1:
                        price.update(gem*int(amount))
                card=cls(color,points,price)
                CARDS[level].append(card)
        
        for level in range(3):
            shuffle(CARDS[level])
        
        decks=[level[:-MAX_OPEN_CARDS] for level in CARDS]
        openCards=[level[-MAX_OPEN_CARDS:] for level in CARDS]
        return decks,openCards
