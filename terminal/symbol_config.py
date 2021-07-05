class SymbolConfig:
    def __init__(self, commission_buy, commission_sell, swap_buy, swap_sell):
        self.commission_buy = commission_buy
        self.commission_sell = commission_sell
        self.swap_buy = swap_buy
        self.swap_sell = swap_sell


symbol_config = {
    'BTCUSD': SymbolConfig(0.01, 0.005, 0, 0),
}
