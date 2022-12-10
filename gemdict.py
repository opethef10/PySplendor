from collections import Counter

GOLD_GEM = 'y'
COLORED_GEMS = 'r', 'g', 'b', 'w', 'k'
ALL_GEMS = COLORED_GEMS + tuple(GOLD_GEM)
COLORS = "❤", "🍏", "💧", "⚪", "🏴", "⭐"


class GemDict(Counter):
    """Counter of gems with count (or price) each"""
    emoji = True
        
    def __str__(self):
        def map_color(gem):
            return COLORS[ALL_GEMS.index(gem)] if self.emoji else gem
        return " ".join(str(amount) + map_color(gem) for gem, amount in self.items())

    def __add__(self, other):
        result = super().__add__(other)
        return GemDict(result)

    def __sub__(self, other):
        result = super().__sub__(other)
        return GemDict(result)

    def total(self):
        """Total count of all gems in set"""
        return sum(self.values())
    
    @classmethod
    def from_rules(cls, max_gems, max_gold):
        return cls(COLORED_GEMS*max_gems + tuple(GOLD_GEM)*max_gold)
