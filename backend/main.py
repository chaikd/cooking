"""
智能厨师
分析上传的图片
查看图片中的菜
根据菜名从网络中搜索菜谱，返回3条数据
聊天记录持久化到数据库


路由
获取聊天列表
获取指定聊天的聊天数据
发送消息到指定聊天
上传图片
"""
from fastapi import APIRouter, FastAPI

# routers
from routers.main import session_router

app = FastAPI()

app.include_router(session_router)
