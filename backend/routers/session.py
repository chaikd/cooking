from functools import partial
from typing import List, Union, Optional, Literal

from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.sse import EventSourceResponse, ServerSentEvent
from pydantic import BaseModel
from pymongo.synchronous.database import Database

from agent.main import AgentService
from mongo.main import mongo_client, checkpoint_db, SESSIONS

router = APIRouter(
    prefix="/api/session",
    responses={404: {"description": "Not found"}},
)

class Session(BaseModel):
    id: str
    session_name: str

class SendSession(BaseModel):
    id: str
    message: str
    type: Literal['text', 'image']


@router.get('/list')
def get_session_list() -> List[Session]:
    session_list = SESSIONS.find()
    return list(session_list)

@router.get('/{session_id}')
def get_session(session_id: str) -> Session:
    session = SESSIONS.find_one({'id': session_id})
    return session

@router.post('/chat', response_class=EventSourceResponse)
def send_session(session_info: SendSession):
    session_id = session_info.id
    session_type = session_info.type
    message = session_info.message
    agent_service = AgentService()
    try:
        res = agent_service.ask(session_type, message, session_id)
        for word in res:
            yield ServerSentEvent(data=word, event="token")
        yield ServerSentEvent(raw_data="[DONE]", event="done")
    except Exception as e:
        yield ServerSentEvent(data=str(e), event="token")
        yield ServerSentEvent(raw_data="[ERROR]", event="error")