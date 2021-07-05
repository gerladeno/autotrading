from tkinter import Tk

from data_provider.ticks_provider import TicksProvider
from strategies.moving_average import MovingAverage
from terminal.app import App
from terminal.engine import Engine


def main_with_ui():
    ds = TicksProvider(real=True)
    root = Tk()
    app = App(ds.symbol, ds.get_ticks())
    root.mainloop()


def main_cli():
    ds = TicksProvider(real=True)
    engine = Engine(ds.get_ticks(), "BTCUSD")
    ma = MovingAverage(1000, engine)
    ma.run()


def main_ui_with_strategy():
    ds = TicksProvider(real=True)
    ma = MovingAverage(10)
    root = Tk()
    app = App(ds.symbol, ds.get_ticks(), ma)
    root.mainloop()


if __name__ == "__main__":
    # main_cli()
    main_with_ui()
    # main_ui_with_strategy()
