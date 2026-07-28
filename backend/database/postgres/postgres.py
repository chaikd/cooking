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
                     CREATE OR REPLACE FUNCTION update_timestamp()
                         RETURNS TRIGGER AS
                     $$
                     BEGIN
                         NEW.update_time = NOW();
                         RETURN NEW;
                     END;
                     $$ LANGUAGE plpgsql;
                """)
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS business.conversations
                    (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        user_id UUID NOT NULL,
                        title VARCHAR(200) NOT NULL,
                        create_time TIMESTAMPTZ DEFAULT NOW(),
                        conversation_id UUID NOT NULL UNIQUE,
                        status VARCHAR(20) DEFAULT 'active',
                        title_generated BOOLEAN DEFAULT FALSE
                        CONSTRAINT status_check CHECK(
                            status IN (
                                'deleted', 'inactive', 'active'
                            )
                        )
                    )
               """)
                conn.execute("""
                     CREATE TABLE IF NOT EXISTS business.conversation_messages
                     (
                         id              UUID PRIMARY KEY,
                         user_id         UUID NOT NULL,
                         content         TEXT NOT NULL,
                         create_time     TIMESTAMPTZ      DEFAULT NOW(),
                         update_time     TIMESTAMPTZ      DEFAULT NOW(),
                         conversation_id UUID NOT NULL REFERENCES business.conversations(conversation_id),
                         role VARCHAR(20) DEFAULT 'user',
                         status VARCHAR(20) DEFAULT 'completed',
                         CONSTRAINT role_check CHECK(
                            role IN(
                                'assistant', 'user', 'thinking'
                            )
                         ),
                         CONSTRAINT  status_check CHECK(
                            status IN(
                                'streaming', 'completed', 'error'
                            )
                         )
                     );
                     CREATE TRIGGER trigger_update_timestamp
                     BEFORE UPDATE
                     ON business.conversation_messages
                     FOR EACH ROW
                     EXECUTE FUNCTION update_timestamp();
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
                pass
                # conn.close()

database = PostgresDB()