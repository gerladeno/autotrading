from enum import Enum


class Trade:
    def __init__(self, volume: float, price: float):
        self.volume = volume
        self.price = price


class Position:
    contract_size = 1

    def __init__(self):
        self.price: float = 0
        self.volume: float = 0
        self.floating: float = 0
        self.margin: float = self.volume * self.contract_size

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
        return profit * self.contract_size

    def update_position(self, bid: float, ask: float):
        if self.volume > 0:
            self.floating = (bid - self.price) * self.volume * self.contract_size
        else:
            self.floating = (ask - self.price) * self.volume * self.contract_size
        self.margin = abs(self.volume) * self.contract_size


class Action(Enum):
    buy = 0
    sell = 1
    deposit = 2
    margin_call = 3


class Operation:
    def __init__(self,
                 action: Action,
                 profit: float = 0,
                 volume_change: float = 0,
                 new_volume: float = 0,
                 deal_price: float = 0,
                 new_avg_price: float = 0):
        self.action = action
        self.profit = profit
        self.volume_change = volume_change
        self.new_volume = new_volume
        self.deal_price = deal_price
        self.new_avg_price = new_avg_price


class Account:
    def __init__(self, balance: float = 0):
        self.balance = balance
        self.position = Position()
        self.equity = balance
        self.leverage = 200
        self.free_margin = 0
        self.history: list[Operation] = []

    def update_account(self, bid: float, ask: float) -> bool:
        self.position.update_position(bid, ask)
        self.equity = self.balance + self.position.floating
        self.free_margin = self.equity - self.position.margin / self.leverage
        if self.equity > 0:
            return True
        else:
            self._margin_call(bid, ask)
            return False

    def trade(self, bid: float, ask: float, volume: float):
        if volume > 0:
            price = ask
        else:
            price = bid
        profit = self.position.trade(Trade(volume, price))
        self._trade_op(volume, price, profit)
        self.balance += profit
        self.update_account(bid, ask)

    def _margin_call(self, bid: float, ask: float):
        if self.position.volume > 0:
            price = bid
        else:
            price = ask
        self.history.append(Operation(Action.margin_call, deal_price=price))

    def _trade_op(self, volume, price, profit):
        if volume > 0:
            action = Action.buy
        else:
            action = Action.sell
        self.history.append(Operation(action, profit, volume, self.position.volume, price, self.position.price))

    def deposit(self, amount: float, bid: float, ask: float):
        self.balance += amount
        self.history.append(Operation(Action.deposit))
