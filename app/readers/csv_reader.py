import duckdb


class CSVReader:

    def __init__(self, path):
        self.con = duckdb.connect()
        self.path = path

        # small sample for type sniff only -- NOT full-file scan.
        # old code used sample_size=-1, forcing a full CSV parse just to
        # detect types, then a SECOND full parse to read data.
        self.scan_expr = f"read_csv_auto('{self.path}', sample_size=20480)"

    def schema(self):
        return self.con.execute(
            f"DESCRIBE SELECT * FROM {self.scan_expr}"
        ).fetchall()

    def aggregate(self, sql_exprs):
        """
        Run ONE aggregate query over the whole file, single pass.
        DuckDB's own engine handles vectorization + multithreading +
        streaming (bounded RAM) internally -- no manual chunking needed.
        """
        query = f"SELECT {', '.join(sql_exprs)} FROM {self.scan_expr}"
        cursor = self.con.execute(query)
        row = cursor.fetchone()
        cols = [d[0] for d in cursor.description]
        return dict(zip(cols, row))