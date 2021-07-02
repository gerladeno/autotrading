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


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account(1001)

    def test_no_margin_call(self):
        self.account.trade(35000, 35050, 2)
        self.assertTrue(self.account.update_account(34550, 34600))

    def test_margin_call(self):
        self.account.trade(35000, 35050, 2)
        self.assertTrue(not self.account.update_account(34549, 34599))

    def test_account_buy_buy(self):
        self.account.trade(35000, 35050, 2)
        self.account.trade(34700, 34750, 1)
        self.assertEqual(self.account.balance, 1001)
        self.assertEqual(self.account.free_margin, 250.985)
        self.assertEqual(self.account.position.price, 34950)
        self.assertEqual(self.account.position.volume, 3)

    def test_account_sell_sell(self):
        self.account.trade(35000, 35050, -2)
        self.account.trade(34700, 34750, -1)
        self.assertEqual(self.account.balance, 1001)
        self.assertEqual(self.account.free_margin, 1450.985)
        self.assertEqual(self.account.position.price, 34900)
        self.assertEqual(self.account.position.volume, -3)

    def test_account_buy_sell(self):
        self.account.trade(35000, 35050, 2)
        self.account.trade(34700, 34750, -1)
        self.assertEqual(self.account.balance, 651)
        self.assertEqual(self.account.free_margin, 300.995)
        self.assertEqual(self.account.position.price, 35050)

    def test_account_buy_sell_turnover(self):
        self.account.trade(35000, 35050, 1)
        self.account.trade(34700, 34750, -2)
        self.assertEqual(self.account.balance, 651)
        self.assertEqual(self.account.free_margin, 600.995)
        self.assertEqual(self.account.position.price, 34700)

    def test_account_sell_buy(self):
        self.account.trade(35000, 35050, -2)
        self.account.trade(34700, 34750, 1)
        self.assertEqual(self.account.balance, 1251)
        self.assertEqual(self.account.free_margin, 1500.995)
        self.assertEqual(self.account.position.price, 35000)

    def test_account_sell_buy_turnover(self):
        self.account.trade(35000, 35050, -1)
        self.account.trade(34700, 34750, 2)
        self.assertEqual(self.account.balance, 1251)
        self.assertEqual(self.account.free_margin, 1200.995)
        self.assertEqual(self.account.position.price, 34750)
