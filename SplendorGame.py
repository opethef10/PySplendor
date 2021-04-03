from Card import Card
from GemDict import GemDict,GOLD_GEM
from Noble import Noble
from Player import Player,HumanPlayer,AIPlayer
from Rules import Rules
from Helper import HELP_STR
from random import shuffle
from itertools import combinations
from dataclasses import dataclass,field
from typing import List

TAKE,RESERVE,PURCHASE,PURCHASE_HAND=('t', 'r', 'p', 'h') #action strings
QUIT,HELP=('quit','help')
EMOJI_ENABLED,EMOJI_DISABLED=('emoji1','emoji0')
SLEEP_ENABLED,SLEEP_DISABLED=("sleep1","sleep0")

@dataclass
class SplendorGame:
    human: int
    ai: int
    winScore: int
    rules: Rules = ...
    nobles: List[Noble] = ...
    decks: List[Card] = ...
    cards: List[Card] = ...
    gems: GemDict = ...
    players: List[Player] = ...
    turn: int = 1
    playerToMove: int = 1
    
    def __post_init__(self):                
        self.rules = Rules(self.human+self.ai,self.winScore)
        self.nobles = Noble.getNobles(self.rules.MAX_NOBLES)
        self.decks, self.cards = Card.getCards(self.rules.MAX_OPEN_CARDS)
        self.gems = GemDict.fromRules(self.rules.MAX_GEMS,self.rules.MAX_GOLD)
        self.players = [HumanPlayer("Player"+str(number)) for number in range(1,self.human+1)]+[AIPlayer("AI"+str(number)) for number in range(1,self.ai+1)]        
        shuffle(self.players)
    
    def start(self):
        print(HELP_STR)
        inp=input("Press ENTER to start game:").replace(" ","")
        for actionString in inp.split(","):
            if actionString in (EMOJI_DISABLED,SLEEP_DISABLED):
                try:
                    self.doAction(None,actionString)
                except AttributeError as err:
                    print(err)
    
    def __repr__(self):
        return f"<SplendorGame with {self.human} human, {self.ai} AI players with winning score {self.winScore}>"
        
    def __str__(self):
        s="#"*50 +"\n"
        s+='TURN:' + str(self.turn) + ', PLAYER:' + str(self.playerToMove) + '\n'        
        s+= 'NOBLES: ' + " ".join(str(noble) for noble in self.nobles) + "\n"
        for n, (cardList,deckList) in enumerate(zip(reversed(self.cards),reversed(self.decks))):
            s += "LVL"+str(3 - n) + "("+ str(len(list(deckList))) +")"+': '
            s += " ".join(str(card) for card in cardList) +"\n"

        s+='\n'
        s += 'GEMS: ' + str(self.gems) + '\n\n'

        for player in self.players:
            s += str(player) +'\n'
        s+="#"*50
        return s 

    def newTableCard(self, level, pos):
        '''Put new card on table if player reserved/purchased card'''
        self.cards[level][pos] = self.decks[level].pop() if self.decks[level] else Card(None)
    
    def checkWin(self):
        for player in self.players:
            if player.score >= self.rules.WIN_SCORE:
                return True
        return False

    def printResults(self):
        def calculateELO(players,score=1,K=40,m=400):
            K = K / (len(players)-1)
            for (player1,player2) in combinations(players,2):
                expected=1/(1+10**((player2.account.ELO-player1.account.ELO)/m))
                gain=round(K*(score-expected))
                player1.gain+=gain
                player2.gain-=gain
            for n,player in enumerate(players,1):
                player.account.ELO+=player.gain
                player.account.totalGames+=1
                if n==1:
                    player.account.win+=1
                else:
                    player.account.lose+=1
        
        standings = sorted(self.players, key=lambda pl:(pl.score,-pl.cards.total), reverse=True)
        calculateELO(standings)
        
        print("RESULTS:")
        for n,player in enumerate(standings,1):
            player.account.save()
            print(f"{n}) {player.name}: {player.score} points, Current ELO: {player.account.ELO} ({player.gain:+})")
        player.account.updateStandings()
    
    def availableCombinations(self):
        '''Available combinations of gems which can be taken'''
        availableGems=list(self.gems)
        if GOLD_GEM in availableGems:
            availableGems.remove(GOLD_GEM)       
        combOf3=list(map("".join,map(sorted,combinations(availableGems,min(3,len(availableGems)))))) 
        combOf2=list(map("".join,map(sorted,combinations(availableGems,min(2,len(availableGems))))))
        combOf1=availableGems
        combOfDouble=[gem*2 for gem,count in self.gems.items() if not (gem==GOLD_GEM) and (count>=4)]
        return list(set(combOf1+combOf2+combOf3+combOfDouble))

    def doAction(self, player, actionString):
        try:
            assert len(actionString)>0
            if actionString == QUIT:
                while True:
                    try:
                        inp=input("You will lose the game, are you sure? (yes/no): ")
                        assert inp in ("yes","no")
                        if inp=="no":
                            break
                        elif inp=="yes":
                            player.score=-1
                            return
                    except AssertionError:
                        print("Invalid input!")
                raise AttributeError
            
            elif actionString == HELP:
                raise AttributeError(HELP_STR)
            
            elif actionString == EMOJI_ENABLED:
                self._emojiSetting(1)
                raise AttributeError("Gem emojis are enabled.")
            
            elif actionString == EMOJI_DISABLED:
                self._emojiSetting(0)
                raise AttributeError("Gem emojis are disabled.")
            
            elif actionString == SLEEP_ENABLED:
                self._AISleepSetting(0.2)
                raise AttributeError(f"AI sleep time is set to 0.2 seconds")
            
            elif actionString == SLEEP_DISABLED:
                self._AISleepSetting(0)
                raise AttributeError(f"AI sleep time is disabled")

            elif actionString[0] == TAKE:
                gemStr = [g for g in actionString[1:]]
                player.takeGems(self,gemStr)
            
            elif actionString[0] == RESERVE:
                assert len(actionString) == 3 
                level = int(actionString[1]) - 1
                pos = int(actionString[2]) - 1
                player.reserve(self,level,pos)

            elif actionString[0] == PURCHASE:
                assert len(actionString) == 3
                level = int(actionString[1]) - 1
                pos = int(actionString[2]) - 1
                player.purchase(self,level,pos)

            elif actionString[0] == PURCHASE_HAND:
                assert len(actionString) == 2
                pos = int(actionString[1]) - 1
                player.purchase(self,None,pos)

            else:
                raise AttributeError('Invalid action type {}'.format(actionString[0]))
        
        except (AssertionError,ValueError):
            raise AttributeError('Invalid action string {}'.format(actionString))

        self.playerToMove = (self.playerToMove + 1) % self.rules.NUM_PLAYERS
        if self.playerToMove == 0:
            self.playerToMove=self.rules.NUM_PLAYERS
        if self.playerToMove == 1: # round end
            self.turn += 1
    
    def _emojiSetting(self,parameter):
        assert parameter in (0,1)
        self.gems.setEmoji(parameter)
        for noble in self.nobles:
            noble.price.setEmoji(parameter)
        for level in self.cards:
            for card in level:
                card.price.setEmoji(parameter)
        for level in self.decks:
            for card in level:
                card.price.setEmoji(parameter)
        for player in self.players:
            player.cards.setEmoji(parameter)
            player.gems.setEmoji(parameter)
            for reservedCard in player.handCards:
                reservedCard.price.setEmoji(parameter)
    
    def _AISleepSetting(self,duration):
        if duration<0:
            raise AttributeError("Sleep parameter can't be negative")
        for player in self.players:
            if player.isAI:
                player.setSleepTime(duration)