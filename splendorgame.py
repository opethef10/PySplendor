"""Main game logic for Splendor board game"""

from dataclasses import dataclass
from itertools import combinations, cycle
from random import shuffle

from card import Card
from gemdict import GemDict, GOLD_GEM
from noble import Noble
from player import Player, HumanPlayer, AIPlayer
from rules import Rules


@dataclass
class SplendorGame:
    human: int = 0
    ai: int = 2
    winScore: int = 21
    rules: Rules = ...
    nobles: list[Noble] = ...
    decks: list[list[Card]] = ...
    cards: list[list[Card]] = ...
    gems: GemDict = ...
    players: list[Player] = ...
    turn: int = 1
    currentPlayer: Player = ...

    def __post_init__(self):
        super().__init__()
        self.rules = Rules(self.human + self.ai, self.winScore)
        self.nobles = Noble.get_nobles(self.rules.NOBLE_AMOUNT)
        self.decks, self.cards = Card.get_cards(self.rules.OPEN_CARDS_PER_LEVEL)
        self.gems = GemDict.from_rules(self.rules.MAX_GEMS_IN_STACK, self.rules.MAX_GOLD)
        self.players = [
            HumanPlayer(f"Player{number + 1}") for number in range(self.human)] + [
            AIPlayer(f"AI{number + 1}") for number in range(self.ai)
        ]
        shuffle(self.players)
        self._playerIterator = cycle(self.players)
        self.currentPlayer = next(self._playerIterator)

    def __repr__(self):
        return f"<SplendorGame with {self.human} human, {self.ai} AI players with winning score {self.winScore}>"

    def __str__(self):
        st = "##################################################\n"
        st += f"TURN:{self.turn}, PLAYER:{self.currentPlayer.name}\n"
        st += f"NOBLES: {' '.join(str(noble) for noble in self.nobles)}\n"
        for level, levelCards in reversed(list(enumerate(self.cards))):
            st += f"LVL{level+1}({len(self.decks[level])}): "
            st += f"{' '.join(map(str, levelCards))}\n"
        st += '\n'
        st += f"GEMS: {self.gems}\n\n"

        for player in self.players:
            st += f"{player}\n"
        st += "##################################################"
        return st

    def new_table_card(self, level, pos):
        """Put new card on table if player reserved/purchased card"""
        self.cards[level][pos] = self.decks[level].pop() if self.decks[level] else Card()

    def move_to_next(self):
        """Move to next player. If every player played their turn, increase the turn count"""
        if self.currentPlayer == self.players[-1]:
            self.turn += 1
        self.currentPlayer = next(self._playerIterator)

    def check_win(self):
        """Check the win condition after each turn"""
        return (
            self.currentPlayer == self.players[-1] and
            any(player.score >= self.rules.WIN_SCORE for player in self.players)
        )

    def players_sorted_by_score(self):
        """Return the list of players sorted by score. If equal, who has fewer cards and hand cards is ahead"""
        return sorted(
            self.players,
            key=lambda p: (p.score, -p.purchasedCards.total(), -len(p.handCards)),
            reverse=True
        )

    def update_elo(self, score=1, k=40, m=400):
        """Update Elo score for each player"""

        standings = self.players_sorted_by_score()
        # Update k factor according to the player count
        k = k / (len(standings) - 1)
        for (player1, player2) in combinations(standings, 2):
            expected = 1 / (1 + 10 ** ((player2.account.elo - player1.account.elo) / m))
            gain = round(k * (score - expected))
            player1.gain += gain
            player2.gain -= gain

        # Update player account files
        for pos, player in enumerate(standings, 1):
            player.account.elo += player.gain
            player.account.totalGames += 1
            if pos == 1:
                player.account.win += 1
            else:
                player.account.lose += 1
            player.account.save()
        player.account.update_standings()

    def print_results(self):
        print("RESULTS:")
        for pos, player in enumerate(self.players_sorted_by_score(), 1):
            print(f"{pos}) {player.name}: {player.score} points, Current Elo: {player.account.elo} ({player.gain:+})")

    def available_combinations(self):
        """Available combinations of gems which can be taken"""
        available_gems = set(self.gems)
        available_gems.discard(GOLD_GEM)
        available_sets = len(available_gems)
        comb_of_3 = set(map("".join, combinations(available_gems, min(3, available_sets))))
        comb_of_2 = set(map("".join, combinations(available_gems, min(2, available_sets))))
        comb_of_1 = available_gems
        comb_of_double = {gem * 2 for gem, count in self.gems.items() if (gem != GOLD_GEM) and (count >= 4)}
        return comb_of_1 | comb_of_2 | comb_of_3 | comb_of_double
