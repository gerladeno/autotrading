class ViewConfig:
    def __init__(self):
        self.FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
        self.WINDOW_WIDTH = 1440
        self.WINDOW_HEIGHT = 900
        self.DELAY = 100
        self.BACKGROUND = "black"
        self.CURSOR = ""
        self.LINE_WIDTH = 2
        self.TICK_SIZE = 2
        self.ACCOUNT_DATA_HEIGHT = 200


class Config:
    def __init__(self):
        self.view = ViewConfig()


config = Config()
