import tkinter

from config import config
from terminal.engine import Engine
from terminal.state import State


class Graph(Engine, tkinter.Canvas):
    def __init__(self, data_source: list[(int, float, float)]):
        tkinter.Canvas.__init__(self,
                                width=config.view.WINDOW_WIDTH,
                                height=config.view.WINDOW_HEIGHT,
                                bg=config.view.BACKGROUND,
                                cursor=config.view.CURSOR)
        Engine.__init__(self, data_source)
        self.padding = 4
        self.width = config.view.WINDOW_WIDTH
        self.height = config.view.WINDOW_HEIGHT
        self.tick_size = config.view.TICK_SIZE
        self.line_width = config.view.LINE_WIDTH
        self.capacity = int((self.width * 0.8 - 2 * self.padding - 2 * self.line_width) / self.tick_size)
        self.ticks: list[State] = []
        self.max = 0
        self.min = 0
        self.position = 0
        self.default_delay = config.view.DELAY
        self.delay = 1
        self.on_pause = False

        self.init()
        self.pack()

    def init(self):
        self.max = self.current_state.ask
        self.min = self.current_state.bid
        self.process_tick()
        self.draw_graph()
        self.dashed_lines()
        self.bind_all("<Key>", self.key_pressed)
        self.after(self.delay, self.step_in)

    def step_in(self):
        if self.position == len(self.ticks):
            if self.get_next_state():
                self.process_tick()
                self.draw_graph()
                self.move_dashed_lines()
                self.after(self.delay, self.step_in)
            else:
                pass
                # sys.exit(0)
        else:
            self.draw_graph()
            self.move_dashed_lines()
            self.after(self.delay, self.step_in)

    def process_tick(self):
        tick = self.states[-1]
        if len(self.ticks) < self.capacity:
            self.ticks.append(tick)
        else:
            self.delay = self.default_delay
            self.ticks.append(tick)
            self.ticks = self.ticks[1:]
        self.position = len(self.ticks)

    def dashed_lines(self):
        x = self.padding + 2 * self.line_width + self.position * self.tick_size + 2
        self.create_line(x, self.padding * 2, x, self.height - self.padding * 2, dash=(5, 2), fill='#FAFAD2', width=1,
                         tag='h_dashed')
        self.create_line(self.padding * 2, self.y_bid(self.ticks[self.position - 1]), self.width - self.padding * 2,
                         self.y_bid(self.ticks[self.position - 1]), dash=(5, 2), fill='#FAFAD2', width=1,
                         tag='bid_dashed')
        self.create_line(self.padding * 2, self.y_ask(self.ticks[self.position - 1]), self.width - self.padding * 2,
                         self.y_ask(self.ticks[self.position - 1]), dash=(5, 2), fill='#FAFAD2', width=1,
                         tag='ask_dashed')
        self.draw_prices()

    def move_dashed_lines(self):
        x = self.padding + 2 * self.line_width + self.position * self.tick_size + 2
        self.moveto("h_dashed", x=x)
        self.moveto("bid_dashed", y=self.y_bid(self.ticks[self.position - 1]))
        self.moveto("ask_dashed", y=self.y_ask(self.ticks[self.position - 1]))
        self.draw_prices()

    def draw_graph(self):
        self.delete("bid", "ask", "ask_price", "bid_price")
        self.create_line(self.padding, self.height - self.padding, self.width - self.padding,
                         self.height - self.padding, width=self.line_width, arrow=tkinter.LAST, fill='#FFD700')
        self.create_line(self.padding, self.height - self.padding, self.padding, self.padding, width=self.line_width,
                         arrow=tkinter.LAST, fill='#FFD700')
        self.calc_min_max()
        for i in range(len(self.ticks)):
            self.draw_tick(self.ticks[i], i)

    def draw_tick(self, tick: State, position: int):
        x = self.padding + 2 * self.line_width + position * self.tick_size
        self.create_line(x, self.y_bid(tick), x + self.tick_size, self.y_bid(tick), fill='#ff0000', tag="bid")
        self.create_line(x, self.y_ask(tick), x + self.tick_size, self.y_ask(tick), fill='#00ff00', tag="ask")

    def draw_prices(self):
        self.create_text(self.padding * 15, self.y_ask(self.ticks[self.position - 1]) - 15,
                         text=str(self.ticks[self.position - 1].ask),
                         fill="#ffffff", tag="ask_price")
        self.create_text(self.padding * 15, self.y_bid(self.ticks[self.position - 1]) - 15,
                         text=str(self.ticks[self.position - 1].bid),
                         fill="#ffffff", tag="bid_price")

    def y_ask(self, tick: State) -> int:
        return 2 * self.padding + int(
            self.height * (1 - (tick.ask - self.min) / (self.max - self.min + 4 * self.padding)))

    def y_bid(self, tick: State) -> int:
        return 2 * self.padding + int(
            self.height * (1 - (tick.bid - self.min) / (self.max - self.min + 4 * self.padding)))

    def key_pressed(self, event: tkinter.Event):
        key = event.keysym
        if key == 'space':
            if not self.on_pause:
                self.on_pause = True
                self.delay = 10000000
            else:
                self.on_pause = False
                self.delay = self.default_delay
                self.step_in()
        elif self.on_pause:
            if key == 'Right':
                if self.position < len(self.ticks):
                    self.position += 1
                self.step_in()
            elif key == 'Left' and self.position > 0:
                self.position -= 1
                self.step_in()

    def calc_min_max(self):
        self.max = self.ticks[0].ask
        self.min = self.ticks[0].bid
        for tick in self.ticks:
            if self.max < tick.ask:
                self.max = tick.ask
            if self.min > tick.bid:
                self.min = tick.bid

    def get_current_state(self) -> State:
        return self.ticks[self.position - 1]


class App(tkinter.Frame):
    def __init__(self, name: str, data_source: list[(int, float, float)]):
        super(App, self).__init__()
        self.master.title(name)
        self.graph = Graph(data_source)
        self.pack()
