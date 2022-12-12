from dataclasses import dataclass, field
from operator import itemgetter
from random import choice, sample
from time import sleep

from account import Account
from gemdict import GemDict, GOLD_GEM, ALL_GEMS
from noble import Noble

TAKE, PURCHASE = ('take ', 'purchase ')  # action strings


@dataclass
class Player:
    name: str
    purchasedCards: GemDict = field(default_factory=GemDict)
    gems: GemDict = field(default_factory=GemDict)
    handCards: list = field(default_factory=list)
    score: int = 0
    gain: int = 0
    account: Account = ...
    sleepTime = 0.2

    def __post_init__(self):
        self.account = Account.load(self.name)
        self.purchasedCards.shape = "▮"

    def __str__(self):
        st = f"{self.name} ({self.account.elo}) | {self.score} points\n"
        st += f"purchased: {self.purchasedCards}\n"
        st += f"gems: {self.gems} ({self.gems.total()})\n"
        st += f"reserved:\n"
        st += '\n'.join(f"{idx}: {card}" for idx, card in enumerate(self.handCards, 1)) + "\n"
        return st

    @property
    def wealth(self):
        return self.purchasedCards + self.gems

    def take_gems(self, game, gem_lst):
        unique_gems = list(set(gem_lst))
        invalid_gems = set(gem_lst) - set(ALL_GEMS)

        if invalid_gems:
            raise ValueError('Invalid gem(s) ' + ", ".join(invalid_gems))
        if GOLD_GEM in gem_lst:
            raise ValueError('You are not allowed to take gold gem')
        if len(gem_lst) > game.rules.MAX_GEMS_TAKE:
            raise ValueError(f"Can't take more than {game.rules.MAX_GEMS_TAKE} gems")
        for gem in gem_lst:
            if game.gems[gem] == 0:
                raise ValueError(f'Not enough {gem} gems on table')

        if len(unique_gems) == 1 and len(gem_lst) != 1:  # all same color
            if len(gem_lst) > game.rules.MAX_SAME_GEMS_TAKE:
                raise ValueError(f"Can't take more than {game.rules.MAX_SAME_GEMS_TAKE} identical gems")
            if game.gems[unique_gems[0]] < game.rules.MIN_SAME_GEMS_STACK:
                raise ValueError(f'Should be at least {game.rules.MIN_SAME_GEMS_STACK} gems in stack')
        if len(unique_gems) > 1 and len(unique_gems) != len(gem_lst):
            raise ValueError('You can either take all identical or all different gems')

        for gem in gem_lst:
            self.gems.update(gem)
            game.gems.subtract(gem)
        overflow = self.gems.total() - game.rules.MAX_PLAYER_GEMS
        if overflow > 0:
            self.remove_gems(game, overflow)

    def reserve(self, game, level, pos):
        if level not in {0, 1, 2}:  # level < 0 or level >= 3:
            raise ValueError(f'Invalid deck level {level + 1}')
        if pos not in range(-1, game.rules.OPEN_CARDS_PER_LEVEL):  # pos < -1 or pos >= len(game.cards[level]):
            raise ValueError(f'Invalid card position {pos + 1}')
        if len(self.handCards) >= game.rules.MAX_HAND_CARDS:
            raise ValueError(f"Player can't reserve more than {game.rules.MAX_HAND_CARDS} cards")

        if pos == -1:  # blind reserve from deck
            if not game.decks[level]:
                raise ValueError(f'Deck {level + 1} is empty')
            card = game.decks[level].pop()
        else:  # reserve from open cards
            card = game.cards[level][pos]
            if card.color is None:
                raise ValueError('The card position is empty')
            game.new_table_card(level, pos)

        self.handCards.append(card)
        if game.gems[GOLD_GEM] > 0:
            self.gems.update(GOLD_GEM)
            game.gems.subtract(GOLD_GEM)
        overflow = self.gems.total() - game.rules.MAX_PLAYER_GEMS
        if overflow > 0:
            self.remove_gems(game, overflow)

    def purchase(self, game, level, pos):
        if level is not None:
            if level not in {0, 1, 2}:
                raise ValueError(f'Invalid deck level {level + 1}')

            if pos not in range(game.rules.OPEN_CARDS_PER_LEVEL):
                raise ValueError(f'Invalid card position {pos + 1}')

            if game.cards[level][pos].color is None:
                raise ValueError('The card position is empty')

            card_to_take = game.cards[level][pos]

        else:
            if pos not in range(len(self.handCards)):
                raise ValueError(f'Invalid card position in hand {pos + 1}')
            card_to_take = self.handCards[pos]

        shortage_gem_dict = card_to_take.price - self.wealth
        gold_to_pay = shortage_gem_dict.total()
        if self.gems[GOLD_GEM] < gold_to_pay:
            raise ValueError("Player can't afford card")
        gold_gem_dict = GemDict(GOLD_GEM * gold_to_pay)
        to_pay = card_to_take.price - self.purchasedCards - shortage_gem_dict + gold_gem_dict

        self.gems.subtract(to_pay)
        game.gems.update(to_pay)
        self.purchasedCards.update(card_to_take.color)
        self.score += card_to_take.points

        if level is None:
            self.handCards.pop(pos)
        else:
            game.new_table_card(level, pos)
        self.get_noble(game.nobles)  # try to get noble

    def get_noble(self, nobles):
        """Attempts to acquire noble card. In case of success removes taken noble from input list"""
        eligible_nobles = [noble for noble in nobles if not noble.price - self.purchasedCards]
        if eligible_nobles:
            selected_noble = choice(eligible_nobles)
            nobles.remove(selected_noble)
            self.score += selected_noble.points

    def possible_moves(self, game):
        return []

    def think(self, move):
        pass

    def remove_gems(self, game, overflow):
        pass


@dataclass
class HumanPlayer(Player):
    def remove_gems(self, game, overflow):
        print(f"{self.name} can't have more than {game.rules.MAX_PLAYER_GEMS} gems")
        while True:
            try:
                remove_str = input(f'{self.name}, remove {overflow} gems from {self.gems}: ')
                assert len(remove_str) == overflow
                if set(remove_str) - set(self.gems):
                    raise ValueError('Invalid gem(s): {}'.format(", ".join(set(remove_str) - set(ALL_GEMS))))
                for gem in set(remove_str):
                    if remove_str.count(gem) > self.gems[gem]:
                        raise ValueError(f"Not enough {gem} gem to remove")
                for gem in set(remove_str):
                    to_remove = remove_str.count(gem)
                    self.gems.subtract(gem * to_remove)
                    game.gems.update(gem * to_remove)
                break
            except AssertionError:
                print(f"Invalid action string '{remove_str}'. You must remove exactly {overflow} gems")
            except ValueError as err:
                print(err)


@dataclass
class AIPlayer(Player):
    def think(self, move):
        print(f"{self.name} is thinking", end="", flush=True)
        for _ in range(3):
            sleep(self.sleepTime)
            print(".", end="", flush=True)
            sleep(self.sleepTime)
        print()
        print(f'{self.name} move: {move}')

    def remove_gems(self, game, overflow):
        while True:
            try:
                remove_str = "".join(sample(set(self.gems), overflow))
                for gem in set(remove_str):
                    if remove_str.count(gem) > self.gems[gem]:
                        raise ValueError(f"Not enough {gem} gem to remove")
                for gem in set(remove_str):
                    to_remove = remove_str.count(gem)
                    self.gems.subtract(gem * to_remove)
                    game.gems.update(gem * to_remove)
                print(self.name + f' removed {overflow} gems: {remove_str}')
                break
            except ValueError as err:
                print(err)

    def possible_moves(self, game):
        gold = self.gems[GOLD_GEM]
        action_scores = [(-100, TAKE)]
        available_comb = game.available_combinations()

        for level, cards in enumerate(game.cards, 1):
            for pos, card in enumerate(cards, 1):
                if card.color is None:
                    continue
                shortage_gem_dict = card.price - self.wealth
                gold_shortage = shortage_gem_dict.total() - gold
                if gold_shortage <= 0:  # affordable card
                    action = PURCHASE + str(level) + str(pos)  #
                    score = card.points + 2
                    action_scores.append((score, action))
                else:
                    short_gems = list(shortage_gem_dict)

                    if len(short_gems) == 1 and shortage_gem_dict[short_gems[0]] > 1:
                        short_gems = [short_gems[0], short_gems[0]]
                    elif len(short_gems) > 3:
                        short_gems = sample(short_gems, 3)
                    elif len(short_gems) < 3:
                        possb = list(game.gems.keys())[:5]
                        possb = list(set(possb) - set(short_gems))
                        short_gems.extend(sample(possb, 3 - len(short_gems)))
                    if "".join(sorted(short_gems)) in available_comb:
                        action = TAKE + ''.join(short_gems)
                        score = -gold_shortage
                        if card.points > 0 and gold_shortage < 3:
                            score += card.points + 2
                        action_scores.append((score, action))
                        available_comb.remove("".join(sorted(short_gems)))

        for comb in available_comb:
            action_scores.append((-60 // (len(comb)), TAKE + comb))
        action_scores = sorted(action_scores, key=itemgetter(0), reverse=True)
        return list(map(itemgetter(1), action_scores))
