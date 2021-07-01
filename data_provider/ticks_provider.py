import csv
import logging


def filter_row(row: list[str]) -> (int, float, float):
    return int(row[3]), float(row[6]), float(row[7])


class TicksProvider:
    def __init__(self, real=False):
        self.source = 'resources/test.csv'
        if real:
            self.source = 'resources/BTCUSD_2021-06-29.csv'
        try:
            with open(self.source, "r") as f:
                line = f.readline().split(',')
                self.symbol = line[5]
                self.data = []
                self.data.append(filter_row(line))
                for row in csv.reader(f, delimiter=','):
                    self.data.append(filter_row(row))

        except FileNotFoundError as e:
            logging.log(logging.FATAL, e)
        except IndexError as e:
            logging.log(logging.FATAL, e)

    def get_ticks(self) -> list[(int, float, float)]:
        for line in self.data:
            yield line


if __name__ == "__main__":
    tp = TicksProvider()
    for i in tp.get_ticks():
        print(i)
