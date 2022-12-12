from dataclasses import dataclass
import json
from pathlib import Path
from random import sample

from gemdict import GemDict

NOBLES_JSON_PATH = Path(__file__).with_name("nobles.json")
NOBLE_POINTS = 3


@dataclass(frozen=True)
class Noble:
    points: int
    price: GemDict
    shape = "▲"

    def __str__(self):
        return ''.join(amount * GemDict.map_color(gem, self.shape) for gem, amount in self.price.items())

    @classmethod
    def get_nobles(cls, max_nobles):
        with NOBLES_JSON_PATH.open() as nobleJsonFile:
            noble_dicts = json.load(nobleJsonFile)
        nobles = [cls(NOBLE_POINTS, GemDict(dct)) for dct in noble_dicts]
        return sample(nobles, max_nobles)
