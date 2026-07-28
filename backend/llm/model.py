import os
from abc import ABC, abstractmethod
from typing import Optional

from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

load_dotenv()


class ModelFactory(ABC):
    @abstractmethod
    def generate(self) -> Optional[BaseChatModel]:
        pass

class ChatModelFactory(ModelFactory):
    def __init__(self):
        super().__init__()

    def generate(self):
        return ChatOpenAI(
            model=os.getenv('MODEL_NAME'),
            openai_api_base=os.getenv('CHAT_MODEL_URL'),
            openai_api_key=os.getenv('CHAT_MODEL_KEY'),
            temperature=0.7,
            max_tokens=4096,
            stream_usage=False,  # 禁用 stream_options，GLM/火山引擎不支持
        )

# 延迟加载：只在首次访问时才创建实例
_chat_model = None

def get_chat_model():
    global _chat_model
    if _chat_model is None:
        _chat_model = ChatModelFactory().generate()
    return _chat_model
