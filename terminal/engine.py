from terminal.state import State
from terminal.account import Account


class Engine:
    def __init__(self, data_source: list[(int, float, float)], symbol: str):
        self.ds = data_source
        self.states: list[State] = []
        self.current_state = State(*next(self.ds))
        self.states.append(self.current_state)
        self.symbol = symbol
        self.account = Account(1000)

    def get_next_state(self) -> bool:
        try:
            self.current_state = State(*next(self.ds))
            self.states.append(self.current_state)
            self.account.update_account(*self.current_state.get_price())
            return True
        except StopIteration:
            return False

    def trade(self, volume: float):
        self.account.trade(self.symbol, *self.current_state.get_price(), 0)
