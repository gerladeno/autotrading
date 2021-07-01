from tkinter import Tk

from data_provider.ticks_provider import TicksProvider
from terminal.app import App


def main():
    ds = TicksProvider()
    root = Tk()
    app = App(ds.symbol, ds.get_ticks())
    root.mainloop()


if __name__ == "__main__":
    main()
