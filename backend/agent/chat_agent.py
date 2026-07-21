from typing import Literal

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from agent.tools.web_search import web_search
from database.postgres.postgres import database
from llm.model import chat_model
from utils.path_tool import get_abs_path


class ChatAgent():
    def __init__(self, server):
        super().__init__()
        self.checkpoint_server = server
        self.model = chat_model
        self.tools = [web_search]
        self.middleware = []

        with open(get_abs_path('prompts/main.md'), 'r', encoding='utf-8') as f:
            res = f.read()
            self.system_prompt = res

        self.agent = create_agent(
            model = self.model,
            system_prompt=self.system_prompt,
            tools = self.tools,
            middleware = self.middleware,
            checkpointer = self.checkpoint_server,
        )

    def stream(self, input: str, type: Literal['text', 'image'], thread_id: str):
        # if type == 'text':
        #     message = {'type': 'text', 'text': input}
        # if type == 'image':
        #     message = {'type': 'image', 'url': input}
        res = self.agent.stream_events({
            'messages': [
                HumanMessage(content=input)
            ]
        }, version="v3", config={"thread_id": thread_id})

        for message in res.messages:
            for delta in message.text:
                yield delta

