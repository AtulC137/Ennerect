import time

from aggregators.count import CountAggregator
from aggregators.sum import SumAggregator
from aggregators.min import MinAggregator
from aggregators.max import MaxAggregator
from aggregators.null_count import NullCountAggregator


NUMERIC_TYPES = {
    "BIGINT",
    "INTEGER",
    "SMALLINT",
    "TINYINT",
    "UBIGINT",
    "UINTEGER",
    "USMALLINT",
    "UTINYINT",
    "FLOAT",
    "DOUBLE",
    "DECIMAL",
}


class Describe:

    def __init__(self, reader):
        self.reader = reader
        self.columns = {}

    def _build(self):

        for name, dtype, *_ in self.reader.schema():

            aggs = [
                CountAggregator(name),
                NullCountAggregator(name),
            ]

            if dtype in NUMERIC_TYPES:
                aggs.extend([
                    SumAggregator(name),
                    MinAggregator(name),
                    MaxAggregator(name),
                ])

            self.columns[name] = {
                "dtype": dtype,
                "aggs": aggs,
            }

    def describe(self):

        start = time.perf_counter()

        self._build()

        chunk_size = 500000

        for batch in self.reader.read_chunks(chunk_size):

            for col in self.columns.values():

                for agg in col["aggs"]:
                    agg.update(batch)

        result = {}

        for name, col in self.columns.items():

            row = {
                "dtype": col["dtype"]
            }

            for agg in col["aggs"]:

                key = agg.__class__.__name__.replace("Aggregator", "").lower()
                row[key] = agg.finalize()

            result[name] = row

        exec_time = round(time.perf_counter() - start, 3)

        return {
            "data": result,
            "metadata": {
                "execution_time_sec": exec_time
            }
        }