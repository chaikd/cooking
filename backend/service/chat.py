from datetime import date
from enum import Enum
from typing import Literal

from bson import timestamp
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
    def chat_stream(self, session_info:SendSession):
        session_id = session_info.id
        session_type = session_info.type
        message = session_info.message

        res = self.chat_agent.stream(thread_id=session_id, type=session_type, input=message)
        return res
    def save_session(self, conversation_id, title, user_id):
         with database.db_conn() as conn:
            conn.execute(f"""
                INSERT TO business.conversations (conversation_id, title, user_id)
                    VALUES({conversation_id, title, user_id})
            """)
