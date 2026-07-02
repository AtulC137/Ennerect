import time


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

    def describe(self):

        start = time.perf_counter()

        schema = self.reader.schema()

        exprs = []
        col_meta = {}

        for name, dtype, *_ in schema:

            safe = f'"{name}"'
            is_numeric = dtype in NUMERIC_TYPES

            # count(col) skips nulls; count(*) - count(col) = null_count.
            # both computed in the SAME scan as sum/min/max below --
            # one query, one pass over the file, DuckDB fuses all
            # aggregates internally.
            exprs.append(f'count({safe}) AS "{name}__count"')
            exprs.append(f'count(*) - count({safe}) AS "{name}__null_count"')

            if is_numeric:
                exprs.append(f'sum({safe}) AS "{name}__sum"')
                exprs.append(f'min({safe}) AS "{name}__min"')
                exprs.append(f'max({safe}) AS "{name}__max"')

            col_meta[name] = {"dtype": dtype, "numeric": is_numeric}

        row = self.reader.aggregate(exprs)

        result = {}

        for name, meta in col_meta.items():

            entry = {
                "dtype": meta["dtype"],
                "count": row[f"{name}__count"],
                "null_count": row[f"{name}__null_count"],
            }

            if meta["numeric"]:
                entry["sum"] = row[f"{name}__sum"]
                entry["min"] = row[f"{name}__min"]
                entry["max"] = row[f"{name}__max"]

            result[name] = entry

        exec_time = round(time.perf_counter() - start, 3)

        return {
            "data": result,
            "metadata": {
                "execution_time_sec": exec_time
            }
        }