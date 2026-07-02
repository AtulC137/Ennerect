import pyarrow.compute as pc


class MinAggregator:

    def __init__(self, column):
        self.column = column
        self.minimum = None

    def update(self, batch):

        value = pc.min(batch.column(self.column)).as_py()

        if value is None:
            return

        if self.minimum is None or value < self.minimum:
            self.minimum = value

    def merge(self, other):

        if other.minimum is None:
            return

        if self.minimum is None or other.minimum < self.minimum:
            self.minimum = other.minimum

    def finalize(self):
        return self.minimum