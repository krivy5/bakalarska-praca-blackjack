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

    def get_regular_move(self, player_value: int) -> tuple[float, GameActions]:
        VALID_ACTIONS = {GameActions.hit, GameActions.stand}
        filtered_records = {record for record in self.records
                            if player_value == record.player_value and
                            record.move in VALID_ACTIONS}

        hit_win = hit_loss = stand_win = stand_loss = 0

        for record in filtered_records:
            if record.move == GameActions.hit and record.outcome == Outcomes.win:
                hit_win = record.count
            elif record.move == GameActions.hit and record.outcome == Outcomes.loss:
                hit_loss = record.count
            elif record.move == GameActions.stand and record.outcome == Outcomes.win:
                stand_win = record.count
            elif record.move == GameActions.stand and record.outcome == Outcomes.loss:
                stand_loss = record.count

        hit_ratio = hit_win / (hit_win + hit_loss) if hit_win > 0 else 0
        stand_ratio = stand_win / (stand_win + stand_loss) if stand_win > 0 else 0

        if hit_ratio == stand_ratio == 0:
            return 0, GameActions.stand

        return (hit_ratio, GameActions.hit) if hit_ratio > stand_ratio \
            else (stand_ratio, GameActions.stand)

    def process_pre_aassigned_outcomes(self, outcome: Outcomes) -> None:
        pre_assigned_records = {record for record in self.records
                                if record.outcome == outcome and
                                (record.player_value, record.move) in self.pre_assigned}
        for record in pre_assigned_records:
            record.add_count()

        self.pre_assigned.clear()



#
# a = History()
# print(a.get_regular_move(player_value=13))
# a.add_to_assign(13, GameActions.hit)
# a.add_to_assign(17, GameActions.stand)
# a.assign_outcomes(Outcomes.win)
#
# a.add_to_assign(13, GameActions.hit)
# a.assign_outcomes(Outcomes.win)
#
# a.add_to_assign(13, GameActions.hit)
# a.add_to_assign(17, GameActions.stand)
# a.assign_outcomes(Outcomes.loss)
#
# print(a.get_regular_move(player_value=17))
