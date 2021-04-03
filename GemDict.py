from collections import Counter

GOLD_GEM = 'y'
GEMS = ('r', 'g', 'b', 'w', 'k', GOLD_GEM) # red, green, blue, white, black, yellow(gold)
COLORS=("❤️","🍏","💧","⚪","🏴","⭐")

class GemDict(Counter):
    '''Counter of gems with count (or price) each'''
    def __init__(self, param=None):
        super().__init__(param)
        self._emoji=1
        
    def __str__(self):
        def mapColor(gem):
            return COLORS[GEMS.index(gem)] if self._emoji else gem
        return " ".join(str(self[gem]) + mapColor(gem) for gem in GEMS if gem in self)
    
    @property
    def total(self):
        '''Total count of all gems in set''' 
        return sum(self.values())
    
    def setEmoji(self,parameter):
        assert parameter in (0,1)
        self._emoji=parameter
    
    @classmethod
    def fromRules(cls,MAX_GEMS,MAX_GOLD):
        return cls(GEMS[:-1]*MAX_GEMS+tuple(GOLD_GEM)*MAX_GOLD)
