from typing import Literal

from pydantic import BaseModel
from starlette.requests import Request

class Session(BaseModel):
    id: str
    name: str

class SendSession(BaseModel):
    id: str
    message: str
    type: Literal['text', 'image']

class ChatService:
    def __init__(self, request: Request):
        self.request = request
    async def chat(self, session_info:SendSession):
        session_id = session_info.id
        session_type = session_info.type
        message = session_info.message

        res = self.request.app.state.chat_agent.stream(thread_id=session_id, type=session_type, input=message)
        return res