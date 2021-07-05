from terminal.engine import Engine
from terminal.state import State

volume = 0.1


class MovingAverage:
    def __init__(self, length: int, engine=None):
        self.length: int = length
        self.engine: Engine = engine
        self.states: list[State] = []
        self.average: float = 0
        self.last_state: State = State(0, 0, 0)

    def run(self):
        while self.engine.get_next_state():
            self.logic()

    def calc_average(self):
        return self.average - (self.last_state.get_mean_price() - self.states[-1].get_mean_price()) / self.length

    def calc_first_average(self):
        v = 0
        for state in self.states:
            v += state.get_mean_price()
        return v / self.length

    def logic(self):
        self.states.append(self.engine.get_current_state())
        if len(self.states) > self.length:
            self.last_state = self.states[0]
            self.states = self.states[-self.length:]
        elif len(self.states) == self.length:
            self.average = self.calc_first_average()
        else:
            return

        new_average = self.calc_average()
        if self.average < self.engine.get_current_state().get_mean_price() < new_average:
            self.engine.trade(-volume)
            print(f"sell {volume}")
            self.engine.account.print_account_data()
        if new_average < self.engine.get_current_state().get_mean_price() < self.average:
            self.engine.trade(volume)
            print(f"buy {volume}")
            self.engine.account.print_account_data()

        self.average = new_average
