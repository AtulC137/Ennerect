import pyarrow.compute as pc


class CountAggregator:

    def __init__(self, column):
        self.column = column
        self.count = 0

    def update(self, batch):

        self.count += pc.count(batch.column(self.column)).as_py()

    def merge(self, other):
        self.count += other.count

    def finalize(self):
        return self.count