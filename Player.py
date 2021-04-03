from GemDict import GemDict,GOLD_GEM,GEMS
from Account import Account
from random import randint,sample
from time import sleep
from operator import itemgetter
from dataclasses import dataclass,field

TAKE,PURCHASE=('t', 'p') #action strings
@dataclass
class Player:
    name: str
    cards: GemDict = field(default_factory=GemDict)
    gems: GemDict = field(default_factory=GemDict)
    handCards: list = field(default_factory=list)
    score: int = 0
    gain: int = 0
    account: Account = ...
    
    def __post_init__(self):
        self.account = Account.load(self.name)
 
    def __str__(self):
        s = self.name + " ("+ str(self.account.ELO) +")"+ ' | ' + str(self.score) + ' points\n'
        s += 'cards: ' + str(self.cards) + '\n'
        s += 'gems: ' + str(self.gems) + ' (' +str(self.gems.total)+')' + '\n'
        s += 'hand: ' + " ".join(str(card) for card in self.handCards)
        s += '\n'
        return s
    
    @property
    def wealth(self):
        return GemDict(self.cards+self.gems)

    def takeGems(self,game,gemStr):
        if set(gemStr)-set(GEMS):
            raise AttributeError('Invalid gem(s) {}'.format(", ".join(set(gemStr)-set(GEMS))))
        if GOLD_GEM in gemStr:
                raise AttributeError('You are not allowed to take gold gem')
        if len(gemStr) > game.rules.MAX_GEMS_TAKE:
            raise AttributeError('Can\'t take more than {} gems'.format(game.rules.MAX_GEMS_TAKE))
        for gem in gemStr:
            if game.gems[gem] == 0:
                raise AttributeError('Not enough {} gems on table'.format(gem))
        
        unique_gems = list(set(gemStr))
        if len(unique_gems) == 1 and len(gemStr) != 1: # all same color
            if len(gemStr) > game.rules.MAX_SAME_GEMS_TAKE: 
                raise AttributeError('Can\'t take more than {} identical gems'.format(game.rules.MAX_SAME_GEMS_TAKE))            
            if game.gems[unique_gems[0]] < game.rules.MIN_SAME_GEMS_STACK:
                raise AttributeError('Should be at least {} gems in stack'.format(game.rules.MIN_SAME_GEMS_STACK))
        if len(unique_gems) > 1 and len(unique_gems) != len(gemStr): 
            raise AttributeError('You can either take all identical or all different gems')
        for gem in gemStr:
            self.gems.update(gem)
            game.gems.subtract(gem)
        overflow=self.gems.total - game.rules.MAX_PLAYER_GEMS
        if overflow>0:
            self.removeGems(game,overflow)
        
    def reserve(self,game,level,pos):
        if level < 0 or level >= 3:
                raise AttributeError('Invalid deck level {}'.format(level + 1))
        if pos < -1 or pos >= len(game.cards[level]):
            raise AttributeError('Invalid card position {}'.format(pos + 1))
        if len(self.handCards) >= game.rules.MAX_HAND_CARDS:
            raise AttributeError('Player can\'t reserve more than {} cards'.format(game.rules.MAX_HAND_CARDS))

        card = None
        if pos >= 0:
            card = game.cards[level][pos]
            if card is None:
                raise AttributeError('Card already taken')
            game.newTableCard(level, pos)
        if pos == -1: # blind reserve from deck
            if not game.decks[level]:
                raise AttributeError('Deck {} is empty'.format(level + 1))
            card = game.decks[level].pop()
        self.handCards.append(card)
        if game.gems[GOLD_GEM] > 0:
            self.gems.update(GOLD_GEM)
            game.gems.subtract(GOLD_GEM)
        overflow=self.gems.total - game.rules.MAX_PLAYER_GEMS
        if overflow>0:
            self.removeGems(game,overflow)

    def purchase(self,game,level,pos):
        if level is not None:
            if level < 0 or level >= 3:
                raise AttributeError('Invalid deck level {}'.format(level + 1))
            
            if pos < 0 or pos >= game.rules.MAX_OPEN_CARDS:
                raise AttributeError('Invalid card position {}'.format(pos + 1))
            
            if game.cards[level][pos].color is None:
                raise AttributeError("Card doesn't exist")
            
            cardToTake = game.cards[level][pos]
        
        else:
            if pos < 0 or pos >= len(self.handCards):
                raise AttributeError('Invalid card position in hand {}'.format(pos + 1))
            cardToTake = self.handCards[pos]
        
        shortageGemDict = GemDict(cardToTake.price - self.wealth)
        gold = self.gems[GOLD_GEM] # gold available 
        goldToPay = shortageGemDict.total
        if gold < goldToPay:
            raise AttributeError('Player can\'t afford card')
        # if player can afford card, do actual payment
        if goldToPay > 0:
            self.gems.subtract(GOLD_GEM*goldToPay)
            game.gems.update(GOLD_GEM*goldToPay)
        for gem, price in cardToTake.price.items():
            if gem in shortageGemDict: # have to pay by gold => new gem count is zero
                game.gems.update(gem*price)
                #self.gems[gem] = 0
                del self.gems[gem]
            else:
                toAdd=price-self.cards[gem]
                if toAdd<0:
                    toAdd=0
                self.gems.subtract(gem*toAdd)
                game.gems.update(gem*toAdd)
        self.cards.update(cardToTake.color)
        self.score += cardToTake.points
        
        if level is not None:
            game.newTableCard(level, pos)
        else:
            self.hand_card.pop(pos)
        self.getNoble(game.nobles) # try to get noble

    def getNoble(self, nobles):
        '''Attempts to acquire noble card. In case of success removes taken noble from input list'''
        noble_list = []
        for n, noble in enumerate(nobles):
            can_afford = True
            for gem, price in noble.price.items():
                if self.cards[gem] < price:
                    can_afford = False
                    break
            if can_afford:
                noble_list.append(n)
        
        if noble_list:
            n = randint(0, len(noble_list)-1)# choose random if more than one available
            noble = nobles.pop(noble_list[n])
            self.score += noble.points
    
    def possibleMoves(self,game):
        pass

@dataclass    
class HumanPlayer(Player):
    isAI: bool = False
    
    def getInput(self,moveSet):
        if self.score<0:
            return TAKE
        return input(self.name + ' move: ')
    
    def removeGems(self,game,overflow):
        print(self.name+" can't have more than {} gems".format(game.rules.MAX_PLAYER_GEMS))
        while True:
            try:
                removeStr=input(self.name + f', remove {overflow} gems from {self.gems}: ')
                assert len(removeStr)==overflow
                if set(removeStr)-set(self.gems):
                    raise AttributeError('Invalid gem(s): {}'.format(", ".join(set(removeStr)-set(GEMS))))
                for gem in set(removeStr):
                    if removeStr.count(gem) > self.gems[gem]:
                        raise AttributeError(f"Not enough {gem} gem to remove")
                for gem in set(removeStr):
                    toRemove=removeStr.count(gem)
                    self.gems.subtract(gem*toRemove)
                    game.gems.update(gem*toRemove)
                break
            except AssertionError:
                print(f"Invalid action string '{removeStr}'. You must remove exactly {overflow} gems")
            except AttributeError as err:
                print(err)
        
@dataclass    
class AIPlayer(Player):
    isAI: bool = True
    _sleepTime: float = 0.2
    
    def setSleepTime(self,duration):
        self._sleepTime=duration
    
    def getInput(self,moveSet):
        actionString=str((moveSet.pop())[1])
        print(f"{self.name} is thinking",end="")
        for _ in range(3):
            sleep(self._sleepTime)
            print(".",end="",flush=True)
            sleep(self._sleepTime)
        print()
        print(f'{self.name} move: {actionString}')
        return actionString
    
    def removeGems(self,game,overflow):
        while True:
            try:
                removeStr="".join(sample(set(self.gems),overflow))
                for gem in set(removeStr):
                    if removeStr.count(gem) > self.gems[gem]:
                        raise AttributeError(f"Not enough {gem} gem to remove")
                for gem in set(removeStr):
                    toRemove=removeStr.count(gem)
                    self.gems.subtract(gem*toRemove)
                    game.gems.update(gem*toRemove)
                print(self.name + f' removed {overflow} gems: {removeStr}')
                break
            except AttributeError as err:
                print(err)
    
    def possibleMoves(self,game):
        gold = self.gems[GOLD_GEM]
        actionScores = [(-100,TAKE)] 
        availableComb=game.availableCombinations()

        for level, cards in enumerate(game.cards,1):
            for pos, card in enumerate(cards,1):
                if card.color is None:
                    continue
                shortageGemDict = GemDict(card.price - self.wealth)
                goldShortage = shortageGemDict.total - gold
                if goldShortage <= 0: # affordable card
                    action=PURCHASE+str(level)+str(pos)#
                    score = card.points+2
                    actionScores.append((score, action))
                else: 
                    shortGems = list(shortageGemDict)

                    if len(shortGems) == 1 and shortageGemDict[shortGems[0]] > 1:
                        shortGems = [shortGems[0], shortGems[0]]
                    elif len(shortGems) > 3:
                        shortGems = sample(shortGems,3)
                    elif len(shortGems)<3:
                        possb=list(game.gems.keys())[:5]
                        possb=list(set(possb)-set(shortGems))
                        shortGems.extend(sample(possb,3-len(shortGems)))
                    if "".join(sorted(shortGems)) in availableComb:
                        action=TAKE+''.join(shortGems)
                        score = -goldShortage
                        if card.points > 0 and goldShortage < 3:
                            score += card.points + 2
                        actionScores.append((score, action))
                        availableComb.remove("".join(sorted(shortGems)))
        
        for comb in availableComb:
            actionScores.append((-60//(len(comb)),TAKE+comb))
        actionScores = sorted(actionScores, key = itemgetter(0))
        return actionScores
        