CARD_RANK_TO_INT = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
                    "7": 7, "8": 8, "9": 9, "T": 10,
                    "J": 10, "Q": 10, "K": 10, "A": 11}

CARD_SUIT_TO_INT = {"c": 1, "d": 2, "h": 3, "s": 4}


class Card:
    def __init__(self, rank, suit):
        if suit not in CARD_SUIT_TO_INT.keys() or rank not in CARD_RANK_TO_INT.keys():
            raise ValueError(f"Suit and rank must be one of {CARD_SUIT_TO_INT.keys()}; "
                             f"{CARD_RANK_TO_INT.keys()}")
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def __repr__(self):
        return f"{self.rank}{self.suit}"

    def __lt__(self, other):
        if self.rank != other.rank:
            return CARD_RANK_TO_INT[self.rank] < CARD_RANK_TO_INT[other.rank]
        return CARD_SUIT_TO_INT[self.suit] < CARD_SUIT_TO_INT[other.suit]

    def __eq__(self, other):
        return True if self.rank == other.rank and self.suit == other.suit else False

    def __hash__(self):
        return hash((self.rank, self.suit))

    def __add__(self, other):
        if isinstance(other, Card):
            return CARD_RANK_TO_INT[other.rank] + CARD_RANK_TO_INT[self.rank]
        elif isinstance(other, int):
            return CARD_RANK_TO_INT[self.rank] + other
        raise NotImplementedError

    def __radd__(self, other):
        if isinstance(other, int):
            return other + CARD_RANK_TO_INT[self.rank]
        raise NotImplementedError

    @property
    def value(self):
        return CARD_RANK_TO_INT[self.rank]

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank
