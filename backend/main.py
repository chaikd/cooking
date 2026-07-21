from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agent.chat_agent import ChatAgent
from database.postgres.checkpoint import checkpoint_manager
from database.postgres.postgres import database
# routers
from routers.main import session_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.initialize()
    app.state.lifespan = lifespan
    checkpoint_manager.initialize()
    app.state.checkpoint_saver = checkpoint_manager.saver
    app.state.chat_agent = ChatAgent(app.state.checkpoint_saver)
    yield
    database.close()

app = FastAPI(
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=["*"],
)

app.include_router(session_router)
