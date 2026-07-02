class NullCountAggregator:

    def __init__(self, column):
        self.column = column
        self.null_count = 0

    def update(self, batch):

        self.null_count += batch.column(self.column).null_count

    def merge(self, other):
        self.null_count += other.null_count

    def finalize(self):
        return self.null_count