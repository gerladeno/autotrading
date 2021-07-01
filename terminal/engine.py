from terminal.state import State


class Engine:
    def __init__(self, data_source: list[(int, float, float)]):
        self.ds = data_source
        self.states: list[State] = []
        self.current_state = State(*next(self.ds))
        self.states.append(self.current_state)

    def get_next_state(self) -> bool:
        try:
            self.current_state = State(*next(self.ds))
            self.states.append(self.current_state)
            return True
        except StopIteration:
            return False
