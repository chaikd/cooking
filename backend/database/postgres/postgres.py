import os
from dotenv import load_dotenv
from psycopg_pool import AsyncConnectionPool, ConnectionPool

load_dotenv()

class PostgresDB:
    poll = None
    def  __init__(self):
        super().__init__()
    def initialize(self):
        poll = ConnectionPool(
            min_size=2,
            max_size=20,
            conninfo=os.getenv('POSTGRES_URL') or ''
        )
        poll.open()
        self.poll = poll
    def get_poll(self):
        return self.poll
    def start(self):
        self.poll.open()
    def close(self):
        self.poll.close()

database = PostgresDB()