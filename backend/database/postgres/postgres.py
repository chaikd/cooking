import os
from contextlib import contextmanager

from dotenv import load_dotenv
from psycopg_pool import ConnectionPool

load_dotenv()

class PostgresDB:
    pool = None
    def  __init__(self):
        super().__init__()
    def initialize(self):
        self.pool = ConnectionPool(
            min_size=2,
            max_size=20,
            conninfo=os.getenv('POSTGRES_URL') or ''
        )
        self.pool.open()
        self.setup()
    def get_pool(self):
        return self.pool
    def start(self):
        self.pool.open()
    def close(self):
        self.pool.close()
    def setup(self):
        with self.db_conn() as conn:
            try:
                conn.execute("""
                     CREATE EXTENSION IF NOT EXISTS pgcrypto
                """)
                conn.execute("""
                     CREATE SCHEMA IF NOT EXISTS business
                """)
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS business.conversations
                    (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        user_id UUID NOT NULL,
                        title varchar(200) NOT NULL,
                        create_time TIMESTAMPTZ DEFAULT NOW(),
                        conversation_id UUID,
                        status varchar(20) DEFAULT 'active',
                        CONSTRAINT status_check CHECK(
                            status IN (
                                'deleted', 'inactive', 'active'
                            )
                        )
                    )
               """)
                conn.commit()
            except Exception as e:
                print(type(e))
                print(e)

    @contextmanager
    def db_conn(self):
        with self.pool.connection() as conn:
            try:
                yield conn
            finally:
                conn.close()

database = PostgresDB()