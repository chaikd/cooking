from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from llm.model import get_chat_model
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate


class ChatLLM:
    def __init__(self):
        self._model = None

    @property
    def model(self):
        if self._model is None:
            self._model = get_chat_model()
        return self._model
    def summary_title(self, input: str):

        # def print_prompt(val):
        #     print(val)
        #     return val
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template('这是一个根据用户输入的内容为用户提供依据现有材料可制作菜谱的应用，并且你很擅长根据用户输入的消息领会别人的意图，根据用户消息，结合领会到的，总结成一句10个字以内的文字作为会话标题。'),
                HumanMessagePromptTemplate.from_template('以下是用户输入的内容：{input_msg}')
            ]
        )
        chain = prompt | self.model | StrOutputParser()
        return chain.invoke({
            'input_msg': input
        })

chat_llm = ChatLLM()