from constants import GameActions, Outcomes


class HistoryRecord:
    def __init__(self, player_value: int, move: GameActions, outcome: Outcomes):
        self.player_value = player_value
        self.move = move
        self.outcome = outcome
        self.count = 0

    def __eq__(self, other):
        if isinstance(other, int):
            return self.player_value == other
        return False

    def __hash__(self):
        return hash(self.player_value)

    def __repr__(self):
        return f"({self.player_value}, {self.move}, {self.outcome}, {self.count})"

    def add_count(self):
        self.count += 1


class History:
    def __init__(self):
        self.outcome_history: list[Outcomes] = []
        self.amount_history: list[int] = []

        self.records = set()
        self.pre_assigned: list[tuple[int, GameActions]] = []

        PLAYER_VALUE_RANGE = range(3, 22)
        for player_value in PLAYER_VALUE_RANGE:
            for action in GameActions:
                for outcome in Outcomes:
                    self.records.add(HistoryRecord(player_value, action, outcome))

    def add_to_outcome_history(self, outcome: Outcomes):
        self.outcome_history.append(outcome)

    def add_to_amount_history(self, amount: int):
        self.amount_history.append(amount)

    def add_to_pre_assigned(self, player_value: int, move: GameActions):
        self.pre_assigned.append((player_value, move))

    def process_pre_aassigned_outcomes(self, outcome: Outcomes) -> None:
        pre_assigned_records = {record for record in self.records
                                if record.outcome == outcome and
                                (record.player_value, record.move) in self.pre_assigned}
        for record in pre_assigned_records:
            record.add_count()

        self.pre_assigned.clear()
