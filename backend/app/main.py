from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db
from .api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create DB tables
    await init_db()
    app.state.engine = None
    app.state.sim_task = None
    yield
    # Shutdown: stop running simulation gracefully
    if app.state.engine:
        await app.state.engine.stop()
    if app.state.sim_task:
        await app.state.sim_task

app = FastAPI(title="Warehouse Simulator API", lifespan=lifespan)

# Allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
