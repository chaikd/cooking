import datetime
from typing import List, Literal

from fastapi import APIRouter
from fastapi.sse import EventSourceResponse, ServerSentEvent
from pydantic import BaseModel
from starlette.requests import Request

from database.mongo.main import SESSIONS
from service.chat import Session, SendSession

router = APIRouter(
    prefix="/api/session",
    responses={404: {"description": "Not found"}},
)

# @router.get('/list')
# def get_session_list() -> List[Session]:
#     session_list = SESSIONS.find()
#     return list(session_list)

@router.get('/list')
def get_session_list(request: Request) -> List[Session]:
    # agent_service = ChatAgent()
    # res = request.app.state.chat_agent.get_messages()
    # print(res)
    # return res
    return []

@router.post('/chat', response_class=EventSourceResponse)
async def send_session(session_info: SendSession,request: Request):

    for word in res:
        yield ServerSentEvent(data=word, event="token")


    # yield ServerSentEvent(raw_data="[DONE]", event="done")
    # try:
    #     res = agent_service.ask(session_type, message, session_id)
    #     for word in res:
    #         yield ServerSentEvent(data=word, event="token")
    #     yield ServerSentEvent(raw_data="[DONE]", event="done")
    # except Exception as e:
    #     yield ServerSentEvent(data=str(e), event="token")
    #     yield ServerSentEvent(raw_data="[ERROR]", event="error")


# @router.post('/save_message', response_class=SendSession)
# def save_session(session_info: SendSession):
#     id = session_info.id
#     type = session_info.type
#     message = session_info.message
#     created_time = datetime.datetime.now()

@router.get('/{session_id}')
def get_session(session_id: str) -> Session | None:
    return []
    # session = SESSIONS.find_one({'id': session_id})
    # return session
