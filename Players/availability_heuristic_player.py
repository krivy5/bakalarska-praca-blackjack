from Players.optimal_player import OptimalPlayer
from hand import PlayerHand
from constants import GameActions, Outcomes

MINIMUM_WIN_RATE = 0.5


class AvailabilityHeuristicPlayer(OptimalPlayer):

    def __init__(self, name: str, start_capital: int):
        super().__init__(name, start_capital)
        self.number_of_influenced_moves = 0

    def want_double_down(self, hand: PlayerHand) -> bool:
        valid_actions = {GameActions.double_down}

        history_win_rate, _recommended_move = self.get_best_move(
            hand.optimal_value, valid_actions)

        if history_win_rate > MINIMUM_WIN_RATE:
            self.number_of_influenced_moves += 1
            return True

        return super().want_double_down(hand)

    def want_split(self, hand: PlayerHand) -> bool:
        valid_actions = {GameActions.split}

        history_win_rate, _recommended_move = self.get_best_move(
            hand.optimal_value, valid_actions)

        if history_win_rate > MINIMUM_WIN_RATE:
            self.number_of_influenced_moves += 1
            return True

        return super().want_split(hand)

    def get_current_action(self, hand: PlayerHand) -> GameActions:
        valid_actions = {GameActions.hit, GameActions.stand}

        history_win_rate, recommended_move = self.get_best_move(
            hand.optimal_value, valid_actions)

        if history_win_rate > MINIMUM_WIN_RATE:
            self.number_of_influenced_moves += 1
            return recommended_move

        return super().get_current_action(hand)

    def get_best_move(self, player_value: int, valid_actions: set[GameActions]) -> (
            tuple)[float, GameActions]:
        filtered_records = {r for r in self.history.records
                            if player_value == r.player_value and r.move in valid_actions}

        counts = self.get_action_outcome_counts(filtered_records)
        ratio_dict = self.build_ratio_dict(counts, valid_actions)

        recommended_action = max(ratio_dict, key=ratio_dict.get)
        return ratio_dict[recommended_action], recommended_action

    @staticmethod
    def get_action_outcome_counts(records):
        return {(r.move, r.outcome): r.count for r in records}

    @staticmethod
    def get_ratio(win_count, loss_count):
        return win_count / (win_count + loss_count) if win_count > 0 else 0

    def build_ratio_dict(self, counts: dict[tuple[GameActions, Outcomes], float],
                         valid_actions: set[GameActions]) -> dict[GameActions, float]:
        ratio_dict = dict()

        for action in valid_actions:
            action_win = counts.get((action, Outcomes.win), 0)
            action_loss = counts.get((action, Outcomes.loss), 0)
            ratio = self.get_ratio(action_win, action_loss)
            ratio_dict[action] = ratio

        return ratio_dict
