class Trade:
    def __init__(self, volume: float, price: float):
        self.volume = volume
        self.price = price


class Position:
    def __init__(self):
        self.price: float = 0
        self.volume: float = 0
        self.profit: float = 0
        self.margin: float = 0

    def trade(self, trade: Trade) -> float:
        profit = 0
        if self.volume == 0:
            self.volume = trade.volume
            self.price = trade.price
        elif self.volume * trade.volume > 0:
            self.price = (self.price * self.volume + trade.price * trade.volume) / (self.volume + trade.volume)
            self.volume = self.volume + trade.volume
        else:
            profit = round((trade.price - self.price) * min(abs(trade.volume), abs(self.volume)), 2)
            if self.volume < 0:
                profit = -profit
            if abs(self.volume) < abs(trade.volume):
                self.price = trade.price
            self.volume += trade.volume
        return profit


class Account:
    def __init__(self, balance: float = 0):
        self.balance = balance
        self.positions = Position()
        self.equity = balance
        self.leverage = 200
        self.margin = 0
