import os
from dotenv import load_dotenv
from psycopg_pool import ConnectionPool

load_dotenv()

class PostgresDB:
    pool = None
    def  __init__(self):
        super().__init__()
    def initialize(self):
        pool = ConnectionPool(
            min_size=2,
            max_size=20,
            conninfo=os.getenv('POSTGRES_URL') or ''
        )
        pool.open()
        self.pool = pool
    def get_pool(self):
        return self.pool
    def start(self):
        self.pool.open()
    def close(self):
        self.pool.close()
    def action(self, cb):
        with self.pool.connection() as conn:
            cb(conn)

database = PostgresDB()