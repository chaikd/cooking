from llm.model import chat_model


class ChatLLM:
    def __init__(self):
        self.model = chat_model
    def summary_title(self, input: str):
        return self.model.invoke(
            input=input,
            prompt='''
                你很擅长根据用户输入的消息领会别人的意图，并根据用户消息结合领会到的，总结成一句10个字以内的文字作为会话标题。
            '''
        )

chat_llm = ChatLLM()