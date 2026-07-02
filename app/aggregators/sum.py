import pyarrow.compute as pc


class SumAggregator:

    def __init__(self, column):
        self.column = column
        self.total = 0

    def update(self, batch):

        chunk_sum = pc.sum(batch.column(self.column)).as_py()

        if chunk_sum is not None:
            self.total += chunk_sum

    def merge(self, other):
        self.total += other.total

    def finalize(self):
        return self.total