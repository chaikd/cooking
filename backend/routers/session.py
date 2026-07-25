import datetime
from typing import List, Literal

from fastapi import APIRouter, Depends
from fastapi.sse import EventSourceResponse, ServerSentEvent
from pydantic import BaseModel
from starlette.requests import Request

from database.mongo.main import SESSIONS
from llm.chat_llm import chat_llm
from service.chat import SessionInfo, SendSession, ChatService

router = APIRouter(
    prefix="/api/session",
    responses={404: {"description": "Not found"}},
)

# @router.get('/list')
# def get_session_list() -> List[Session]:
#     session_list = SESSIONS.find()
#     return list(session_list)

@router.get('/list')
def get_session_list(request: Request) -> List[SessionInfo]:
    # agent_service = ChatAgent()
    # res = request.app.state.chat_agent.get_messages()
    # print(res)
    # return res
    return []

def save_session(session_info: SendSession, chat_service):
    # 通过输入调用ai获取新的标题
    input = session_info.message
    id = session_info.id
    title = chat_llm.summary_title(input)
    chat_service.save_session(title = title, user_id='system_user', conversation_id=id)

@router.post('/chat')
async def send_session(session_info: SendSession, chat_service = Depends(ChatService)):
    # 异步保存聊天信息
    save_session(session_info, chat_service)
    # 通过chat_agent获取聊天消息流
    res = chat_service.chat_stream(session_info)
    for word in res:
        print(word)
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
def get_session(session_id: str) -> list[SessionInfo]:
    return []
    # session = SESSIONS.find_one({'id': session_id})
    # return session
