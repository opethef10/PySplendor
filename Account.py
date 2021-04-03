import os,json
from operator import attrgetter
from dataclasses import dataclass,field

accountsDir = os.path.join(os.path.dirname(__file__), "Accounts")
os.makedirs(accountsDir,exist_ok=True)

@dataclass
class Account:
    name: str
    ELO: int = 1500
    totalGames: int = 0
    win: int = 0
    lose: int = 0

    def __str__(self):
        return f"{self.name}: {self.ELO}, Total Games: {self.totalGames}, Win: {self.win}, Lose: {self.lose}"

    def save(self):
        accountFilePath = os.path.join(accountsDir, f"{self.name}.json")
        with open(accountFilePath, 'w') as accountFile:
            json.dump(self.__dict__, accountFile, indent=4) 
    
    @classmethod
    def load(cls,name):
        accountFilePath = os.path.join(accountsDir, f"{name}.json")
        try:
            with open(accountFilePath, 'r') as accountFile:
                jsonDict = json.load(accountFile)
                return cls(**jsonDict)

        except FileNotFoundError:
            return cls(name)
    
    @staticmethod
    def updateStandings():
        standingsFilePath=os.path.join(accountsDir, "standings.txt")
        standings=sorted([Account.load(os.path.splitext(filepath)[0]) for filepath in os.listdir(accountsDir) if filepath.endswith(".json")],
            key=attrgetter("ELO"),reverse=True)
        with open(standingsFilePath, 'w') as standingsFile:
            for acc in standings:
                print(acc,file=standingsFile)