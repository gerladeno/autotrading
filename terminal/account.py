from enum import Enum
from terminal.symbol_config import symbol_config, SymbolConfig


class Trade:
    def __init__(self, volume: float, price: float):
        self.volume = volume
        self.price = price


class Position:
    contract_size = 1

    def __init__(self, symbol: str):
        self.price: float = 0
        self.volume: float = 0
        self.floating: float = 0
        self.margin: float = self.volume * self.contract_size
        self.config: SymbolConfig = symbol_config[symbol]

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
        profit += self._charge_commission(trade.volume)
        return profit * self.contract_size

    def update_position(self, bid: float, ask: float):
        if self.volume > 0:
            self.floating = (bid - self.price) * self.volume * self.contract_size
        else:
            self.floating = (ask - self.price) * self.volume * self.contract_size
        self.margin = abs(self.volume) * self.contract_size

    def _charge_commission(self, volume: float) -> float:
        if volume > 0:
            return -volume * self.config.commission_buy
        else:
            return volume * self.config.commission_sell


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
        self.positions: dict[str:Position] = {}
        self.equity = balance
        self.leverage = 200
        self.free_margin = 0
        self.history: list[Operation] = []

    def update_account(self, bid: float, ask: float) -> bool:
        for symbol in self.positions:
            self.positions[symbol].update_position(bid, ask)
            self.equity = self.balance + self.positions[symbol].floating
            self.free_margin = self.equity - self.positions[symbol].margin / self.leverage
            if self.equity <= 0:
                self._margin_call(symbol, bid, ask)
                return False
        return True

    def trade(self, symbol: str, bid: float, ask: float, volume: float):
        if symbol not in self.positions:
            self.positions[symbol] = Position(symbol)
        if volume > 0:
            price = ask
        else:
            price = bid
        profit = self.positions[symbol].trade(Trade(volume, price))
        self._trade_op(symbol, volume, price, profit)
        self.balance += profit
        self.update_account(bid, ask)

    def _margin_call(self, symbol: str, bid: float, ask: float):
        if self.positions[symbol].volume > 0:
            price = bid
        else:
            price = ask
        self.history.append(Operation(Action.margin_call, deal_price=price))

    def _trade_op(self, symbol: str, volume: float, price: float, profit: float):
        if volume > 0:
            action = Action.buy
        else:
            action = Action.sell
        self.history.append(
            Operation(action, profit, volume, self.positions[symbol].volume, price, self.positions[symbol].price))

    def deposit(self, amount: float):
        self.balance += amount
        self.history.append(Operation(Action.deposit))

    def print_account_data(self):
        print(f"balance: {self.balance:0.2f}\nequity: {self.equity:0.2f}\nfree margin: {self.free_margin:0.2f}")
        for symbol in self.positions:
            print(f"price: {self.positions[symbol].price:0.5f}\nvolume: {self.positions[symbol].volume:0.2f}\n"
                  f"floating: {self.positions[symbol].floating:0.2f}")
