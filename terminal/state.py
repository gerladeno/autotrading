import datetime

from config import config


class Time:
    def __init__(self, unix: int):
        self.unix = unix

    def pretty(self) -> str:
        return datetime.datetime.utcfromtimestamp(self.unix / 1e9).strftime(fmt=config.view.FMT)


class State:
    def __init__(self, unix: int, bid: float, ask: float):
        self.bid = bid
        self.ask = ask
        self.timestamp = Time(unix)

    def get_price(self) -> (float, float):
        return self.ask, self.bid
