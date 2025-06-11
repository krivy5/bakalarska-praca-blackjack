from card import Card
from constants import ACES, BLACKJACK


class Hand:

    def __init__(self):
        self.cards = []

    def __str__(self):
        return f"({self.cards})"

    def __repr__(self):
        return f"({self.cards})"

    def __iter__(self):
        return iter(self.cards)

    @property
    def valid(self):
        return self.optimal_value <= BLACKJACK

    @property
    def optimal_value(self) -> int:
        values = self.possible_values
        maximum = max(values, default=None)
        return max([val for val in values if val <= BLACKJACK], default=maximum)

    @property
    def possible_values(self) -> list[int]:
        num_of_aces = sum(1 for card in self.cards if card in ACES)
        evaluated = sum(self.cards)
        return [evaluated - 10 * i for i in range(num_of_aces + 1)]

    @property
    def first_card(self) -> Card:
        if self.cards:
            return self.cards[0]

    @property
    def second_card(self) -> Card:
        if len(self.cards) >= 2:
            return self.cards[1]

    def clear(self) -> None:
        self.cards = []

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def set_cards(self, cards: list[Card]) -> None:
        self.cards = list(cards)


class PlayerHand(Hand):
    def __init__(self):
        super().__init__()
        self.amount = 0

    @property
    def win_amount(self) -> int:
        return self.amount * 2

    @property
    def draw_amount(self) -> int:
        return self.amount

    def contains_rank(self, rank: str) -> bool:
        return rank in [card.rank for card in self.cards]

    def equal_start_hand(self) -> bool:
        return self.cards[0].rank == self.cards[1].rank \
            if len(self.cards) == 2 else False

    def set_amount(self, amount: int) -> None:
        self.amount = amount
