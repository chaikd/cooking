from datetime import datetime

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
import os
from agent.tools.web_search import web_search
from langgraph.checkpoint.mongodb import MongoDBSaver

from mongo.main import mongo_client, SESSIONS
from utils.path_tool import get_abs_path

load_dotenv()

class AgentService:
  def __init__(self):
    model = ChatOpenAI(
      openai_api_base=os.getenv('CHAT_MODEL_URL'),
      openai_api_key=os.getenv('CHAT_MODEL_KEY'),
      model=os.getenv('MODEL_NAME'),
      model_kwargs={"parallel_tool_calls": False}
    )
    self.checkpointer = MongoDBSaver(mongo_client)

    with open(get_abs_path('prompts/main.md'), 'r', encoding='utf-8') as f:
      text = f.read()
      self.agent = create_agent(
        model=model,
        system_prompt=text,
        tools=[web_search],
        # LangSmith测试需要注释
        checkpointer=self.checkpointer
      )
  def ask(self, type: str, input: str, thread_id: str):
    session_name = input
    if type == 'text':
      message = {'type': 'text', 'text': input}
      session_name = input
    if type == 'image':
      message = {'type': 'image', 'url': input}
      session_name = f'图片分析{datetime.now().strftime("%Y:%m:%d %H:%M:%S")}'
    the_one = SESSIONS.find_one({'thread_id': thread_id})
    if not the_one:
      SESSIONS.insert_one({'thread_id': thread_id, 'session_name': session_name})
    res = self.agent.stream_events({
      'messages': [
        HumanMessage([message])
      ]
    }, version="v3", config={"thread_id": thread_id})
    # for message in res['messages']:
    #   if message.content:
    #     print(type(message).__name__, message.content)
    # return res['messages'][-1].content
    for message in res.messages:
      for delta in message.text:
        # print(delta, end="", flush=True)
        yield delta
  # def get_messages(self):
  #   config = {"configurable": {"thread_id": ""}}
  #   print(list(self.checkpointer.list(config)))
# LangSmith 测试代码开始
# agent_service = AgentService()
# agent = agent_service.agent
# LangSmith 测试代码结束

if __name__ == '__main__':
  service = AgentService()
  res = service.ask(type='text', input='茄子 青椒 豆腐 菠菜', thread_id='thread_id_112')
  # res = service.ask(type='image', input='https://www.magnific.com/zh/%E5%85%8D%E8%B2%BB%E5%9C%96%E7%89%87/arrangement-different-foods-organized-fridge_18392053.htm#fromView=keyword&page=1&position=0&query=%E5%86%B0%E7%AE%B1%E9%A3%9F%E7%89%A9')
  # res = service.ask(type='text', input='第一名方案可以，再详细讲解一下', thread_id='thread_id_111')
  for delta in res:
    print(delta, end='', flush=True)
  # res = service.agent.stream_events({
  #   'messages': [
  #     HumanMessage('茄子 青椒 豆腐 菠菜')
  #   ]
  # }, version="v3")
  # # for message in res['messages']:
  # #   if message.content:
  # #     print(type(message).__name__, message.content)
  # for message in res.messages:
  #   for delta in message.text:
  #     print(delta, end="", flush=True)