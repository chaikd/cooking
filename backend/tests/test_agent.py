from typing import Literal

from agent.chat_agent import ChatAgent
from database.postgres.checkpoint import checkpoint_manager
from database.postgres.postgres import database
from enum import Enum

database.initialize()
checkpoint_manager.initialize()
checkpoint_saver = checkpoint_manager.saver
chat_agent = ChatAgent(checkpoint_saver)
session_info: {
    'id': str,
    'type': Literal['text', 'image'],
    'message': str,
} = {
    'id': "12231qwhgfd",
    "type": 'text',
    "message": "茄子 青椒 青西红柿"
}
res = chat_agent.stream(thread_id=session_info['id'], type=session_info['type'], input=session_info['message'])
for word in res:
    print(word, end='', flush=True)
database.close()