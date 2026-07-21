import os
from abc import ABC, abstractmethod
from typing import Optional

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI


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
        )

chat_model = ChatModelFactory().generate()
