from dataclasses import dataclass
import json
from operator import attrgetter
from pathlib import Path

ACCOUNTS_DIR = Path(__file__).parent / "accounts"
ACCOUNTS_DIR.mkdir(exist_ok=True)
STANDINGS_PATH = ACCOUNTS_DIR / "standings.txt"


@dataclass
class Account:
    name: str
    elo: int = 1500
    totalGames: int = 0
    win: int = 0
    lose: int = 0

    def __str__(self):
        return f"{self.name}: {self.elo}, Total Games: {self.totalGames}, Win: {self.win}, Lose: {self.lose}"

    def save(self):
        account_file_path = ACCOUNTS_DIR / f"{self.name}.json"
        with account_file_path.open('w') as accountFile:
            json.dump(vars(self), accountFile, indent=4)
            accountFile.write("\n")
    
    @classmethod
    def load(cls, name):
        account_file_path = ACCOUNTS_DIR / f"{name}.json"
        try:
            with account_file_path.open() as accountFile:
                account_dict = json.load(accountFile)
            return cls(**account_dict)

        except FileNotFoundError:
            return cls(name)
    
    @staticmethod
    def update_standings():
        standings = sorted(
            (
                Account.load(filepath.stem)
                for filepath
                in ACCOUNTS_DIR.glob("*.json")
            ),
            key=attrgetter("elo"),
            reverse=True
        )
        with STANDINGS_PATH.open('w') as standingsFile:
            for acc in standings:
                print(acc, file=standingsFile)
