from datetime import date, datetime
from enum import Enum
from typing import Literal

from bson import timestamp
from psycopg.rows import dict_row
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from agent.chat_agent import chat_agent
from database.postgres.postgres import database

class SessionStatus(str, Enum):
    DELETED = 'deleted'
    INACTIVE = 'inactive'
    ACTIVE = 'active'

class SessionInfo(BaseModel):
    id: str
    title: str
    status: SessionStatus = 'active'
    user_id: str | None = None
    create_time: str | None = None
    conversation_id: str | None = None

class SendSession(BaseModel):
    id: str
    message: str
    type: Literal['text', 'image']

class ChatService:
    def __init__(self):
        self.chat_agent = chat_agent
    def chat_stream(self, session_info:SendSession) -> Stream:
        session_id = session_info.id
        session_type = session_info.type
        message = session_info.message

        res = self.chat_agent.stream(thread_id=session_id, type=session_type, input=message)
        return res
    def save_session(self, conversation_id: str, title: str, user_id: str):
         with database.db_conn() as conn:
            res = conn.execute("""
                INSERT INTO business.conversations (conversation_id, title, user_id)
                    VALUES(%s, %s, %s)
                ON CONFLICT (conversation_id)
                DO NOTHING
            """, (conversation_id,title,user_id))
            conn.commit()
            print(res)
    def update_session(self, conversation_id: str, title: str):
        with database.db_conn() as conn:
            conn.execute("""
               UPDATE business.conversations
                SET title = %s,
                    title_generated = FALSE
                WHERE conversation_id = %s
           """,(title, conversation_id))
            conn.commit()
    def save_message(self, message_id,user_id, content, conversation_id, role):
        with database.db_conn() as conn:
            conn.execute("""
                INSERT INTO business.conversation_messages (id,user_id, content, conversation_id,role)
                    VALUES (%s, %s, %s, %s, %s)
            """, (message_id,user_id, content, conversation_id, role))
            conn.commit()
    def update_message(self, message_id, content, status):
        with database.db_conn() as conn:
            conn.execute("""
                UPDATE business.conversation_messages
                    SET content = %s,
                        status = %s
                    WHERE id = %s
            """, (content, status, message_id))
            conn.commit()
    def get_session_list(self):
        with database.db_conn() as conn:
            res = conn.execute("""
               SELECT 
                id::TEXT AS id,
                conversation_id::TEXT AS conversation_id,
                title,
                status
                FROM business.conversations
                ORDER BY create_time DESC
           """)
            props = [desc.name for desc in res.description]
            result = [
                dict(zip(props, row)) for row in res.fetchall()
            ]
            return result
    def get_message_list(self, conversation_id):
        with database.db_conn() as conn:
            res = conn.execute("""
                SELECT
                    id::TEXT AS id,
                    conversation_id::TEXT AS conversation_id,
                    content,
                    status,
                    role
                FROM business.conversation_messages
                WHERE conversation_id = %s
                ORDER BY update_time ASC
            """, (conversation_id,))
            props = [desc.name for desc in res.description]
            result = [
                dict(zip(props, row)) for row in res.fetchall()
            ]
            return result