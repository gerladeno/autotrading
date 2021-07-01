import unittest
from terminal.account import Account, Position, Trade


class TestPosition(unittest.TestCase):
    def setUp(self):
        self.position = Position()

    def test_buy_buy(self):
        first_trade = Trade(100, 35000.4)
        second_trade = Trade(50, 34000.2)
        self.assertEqual(self.position.trade(first_trade), 0)
        self.assertEqual(self.position.trade(second_trade), 0)
        self.assertEqual(self.position.volume, 150)
        self.assertEqual(self.position.price, 34667.0)

    def test_sell_sell(self):
        first_trade = Trade(-100, 35000.4)
        second_trade = Trade(-50, 34000.2)
        self.assertEqual(self.position.trade(first_trade), 0)
        self.assertEqual(self.position.trade(second_trade), 0)
        self.assertEqual(self.position.volume, -150)
        self.assertEqual(self.position.price, 34667.0)

    def test_buy_sell(self):
        first_trade = Trade(100, 35000.4)
        second_trade = Trade(-50, 34000.2)
        self.assertEqual(self.position.trade(first_trade), 0)
        self.assertEqual(self.position.trade(second_trade), -50010.0)
        self.assertEqual(self.position.volume, 50)
        self.assertEqual(self.position.price, 35000.4)

    def test_buy_sell_turnover(self):
        first_trade = Trade(50, 34000.2)
        second_trade = Trade(-100, 35000.4)
        self.assertEqual(self.position.trade(first_trade), 0)
        self.assertEqual(self.position.trade(second_trade), 50010.0)
        self.assertEqual(self.position.volume, -50)
        self.assertEqual(self.position.price, 35000.4)

    def test_sell_buy(self):
        first_trade = Trade(-100, 35000.4)
        second_trade = Trade(50, 34000.2)
        self.assertEqual(self.position.trade(first_trade), 0)
        self.assertEqual(self.position.trade(second_trade), 50010.0)
        self.assertEqual(self.position.volume, -50)
        self.assertEqual(self.position.price, 35000.4)

    def test_sell_buy_turnover(self):
        first_trade = Trade(-50, 35000.4)
        second_trade = Trade(100, 34000.2)
        self.assertEqual(self.position.trade(first_trade), 0)
        self.assertEqual(self.position.trade(second_trade), 50010.0)
        self.assertEqual(self.position.volume, 50)
        self.assertEqual(self.position.price, 34000.2)
