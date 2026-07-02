import pyarrow.compute as pc


class MaxAggregator:

    def __init__(self, column):
        self.column = column
        self.maximum = None

    def update(self, batch):

        value = pc.max(batch.column(self.column)).as_py()

        if value is None:
            return

        if self.maximum is None or value > self.maximum:
            self.maximum = value

    def merge(self, other):

        if other.maximum is None:
            return

        if self.maximum is None or other.maximum > self.maximum:
            self.maximum = other.maximum

    def finalize(self):
        return self.maximum