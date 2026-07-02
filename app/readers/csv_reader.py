import duckdb


class CSVReader:

    def __init__(self, path):
        self.con = duckdb.connect()
        self.path = path

        # build query ONCE (no re-execution per batch)
        self.query = f"""
            SELECT *
            FROM read_csv_auto(
                '{self.path}',
                sample_size=-1
            )
        """

    def schema(self):

        return self.con.execute(f"""
            DESCRIBE {self.query}
        """).fetchall()

    def read_chunks(self, chunk_size):

        reader = self.con.execute(self.query)

        batches = reader.fetch_record_batch(rows_per_batch=chunk_size)

        yield from batches