from dataclasses import dataclass
from typing import List, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.sse import EventSourceResponse, ServerSentEvent
from uuid_utils.compat import uuid7

from llm.chat_llm import chat_llm
from service.chat import SessionInfo, SendSession, ChatService
from utils.camelize import camelize


@dataclass
class SaveMessageInfo:
    message_id: UUID
    content: str = ''
    conversation_id: str = ''
    status: Literal['streaming', 'completed', 'error'] = 'streaming'
    role: Literal['user', 'assistant'] = 'user'
@dataclass
class SaveSessionInfo:
    id: str
    message: str

router = APIRouter(
    prefix="/api/session",
    responses={404: {"description": "Not found"}},
)

@router.get('/list')
def get_session_list(chat_service = Depends(ChatService)):
    res = chat_service.get_session_list()
    return camelize(res)

def save_session(session_info: SaveSessionInfo, chat_service):
    # 通过输入调用ai获取新的标题
    title = session_info.message
    id = session_info.id
    chat_service.save_session(title = title, user_id='20c5fe09-b802-4d7c-9c77-173f8d5e3b2b', conversation_id=id)
def update_session(session_info: SaveSessionInfo, chat_service):
    # 通过输入调用ai获取新的标题
    input = session_info.message
    id = session_info.id
    title = chat_llm.summary_title(input)
    chat_service.update_session(title=title, conversation_id=id)

def save_message(session_info: SaveMessageInfo, type: Literal['update', 'insert'], chat_service):
    user_id='20c5fe09-b802-4d7c-9c77-173f8d5e3b2b'
    conversation_id = session_info.conversation_id
    content = session_info.content
    message_id = session_info.message_id
    status = session_info.status or 'streaming'
    role = session_info.role
    arg = {
        'message_id': message_id,
        'user_id': user_id,
        'content': content,
        'conversation_id': conversation_id,
        'status': status,
        'role': role
    }
    if type == 'insert':
        insert_arg = {k: arg[k] for k in[ 'message_id','user_id', 'content', 'conversation_id', 'role']}
        chat_service.save_message(**insert_arg)
    elif type == 'update':
        update_arg = {k: arg[k] for k in ['status', 'message_id', 'content']}
        chat_service.update_message(**update_arg)

@router.post('/chat', response_class=EventSourceResponse)
async def send_session(
    session_info: SendSession,
    background_tasks: BackgroundTasks,
    chat_service = Depends(ChatService)
):
    save_session(SaveSessionInfo(
        id=session_info.id,
        message=session_info.message
    ), chat_service)
    # 后台异步更新会话信息
    background_tasks.add_task(update_session, SaveSessionInfo(
        id=session_info.id,
        message=session_info.message
    ), chat_service)
    # 异步保存message
    user_message_id = uuid7()
    save_message(
        SaveMessageInfo(
            content=session_info.message,
            conversation_id=session_info.id,
            message_id=user_message_id,
            role='user'
        ), type='insert', chat_service=chat_service
    )
    ai_message_id = uuid7()
    save_message(SaveMessageInfo(
        content= '',
        conversation_id= session_info.id,
        message_id= ai_message_id,
        status='streaming',
        role= 'assistant'
    ), type='insert', chat_service=chat_service)
    res = chat_service.chat_stream(session_info)
    content = ''

    for word in res:
        content += word
        yield ServerSentEvent(data=word, event="token")
        background_tasks.add_task(save_message, SaveMessageInfo(
            content= content,
            message_id= ai_message_id,
        ), type='update',chat_service = chat_service)
    yield ServerSentEvent(data="[DONE]", event="done")
    background_tasks.add_task(save_message, SaveMessageInfo(
        content= content,
        message_id= ai_message_id,
        status= 'completed'
    ), type='update', chat_service=chat_service)

@router.get('/{session_id}')
def get_message_list(session_id: str, chat_service = Depends(ChatService)):
    session_list = chat_service.get_message_list(session_id)
    return camelize(session_list)
