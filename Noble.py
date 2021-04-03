from GemDict import GemDict
from random import sample
from dataclasses import dataclass

@dataclass(frozen=True)
class Noble:
    points: int
    price: GemDict

    def __str__(self):
        return '[' + str(self.points) + '|' + str(self.price) + ']'

    @classmethod
    def getNobles(cls,MAX_NOBLES):
        NOBLES_AS_STRLIST=['[3|r4g4]', '[3|g4b4]', '[3|b4w4]', '[3|w4k4]', '[3|k4r4]', '[3|r3g3b3]', '[3|b3g3w3]', '[3|b3w3k3]', '[3|w3k3r3]', '[3|k3r3g3]']
        NOBLES=[]
        for string in NOBLES_AS_STRLIST:
            assert len(string) >= 8
            points = int(string[1])
            num_gems = (len(string) - 4)//2
            assert num_gems in (2,3)
            price = GemDict()
            for n in range(num_gems):
                gem = string[2*n + 3]
                count = int(string[2*n + 4])
                price.update(gem*count)
            NOBLES.append(Noble(points,price))
        return sample(NOBLES, MAX_NOBLES)
