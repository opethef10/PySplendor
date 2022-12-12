from collections import Counter

from termcolor import colored
import colorama
colorama.init(strip=False)

ALL_GEMS = 'r', 'g', 'b', 'w', 'k', 'y'
COLORS = "red", "green", "blue", "white", "grey", "yellow"
COLORDICT = dict(zip(ALL_GEMS, COLORS))
COLORED_GEMS, GOLD_GEM = ALL_GEMS[:-1], ALL_GEMS[-1]


class GemDict(Counter):
    """Counter of gems with count (or price) each"""
    shape = "◉"
        
    def __str__(self):
        return " ".join(amount * self.map_color(gem, self.shape) for gem, amount in self.items() if amount)

    def __add__(self, other):
        result = super().__add__(other)
        return GemDict(result)

    def __sub__(self, other):
        result = super().__sub__(other)
        return GemDict(result)

    @staticmethod
    def map_color(gem, shape):
        return colored(shape, COLORDICT[gem], attrs=["bold"])

    def total(self):
        """Total count of all gems in set"""
        return sum(self.values())
    
    @classmethod
    def from_rules(cls, max_gems, max_gold):
        return cls(COLORED_GEMS*max_gems + tuple(GOLD_GEM)*max_gold)
