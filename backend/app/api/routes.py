import asyncio
from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import AsyncSessionLocal
from ..config import SimConfig
from ..models import SimulationRun, RobotEvent
from ..services.analytics import get_run_analytics
from ..simulation.engine import SimulationEngine
from .websocket import manager

router = APIRouter()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/simulation/start")
async def start_simulation(request: Request, config: SimConfig = None):
    app_state = request.app.state
    if app_state.engine and app_state.engine.running:
        return {"status": "error", "message": "Simulation already running"}
        
    if not config:
        config = SimConfig()
        
    # the frontend needs the connection early
    engine = SimulationEngine(config, None, manager.broadcast) 
    app_state.engine = engine
    app_state.sim_task = asyncio.create_task(engine.start())
    
    return {"status": "ok", "run_id": engine.run_id}

@router.post("/simulation/stop")
async def stop_simulation(request: Request):
    app_state = request.app.state
    if not app_state.engine or not app_state.engine.running:
        return {"status": "error", "message": "No running simulation"}
        
    await app_state.engine.stop()
    if app_state.sim_task:
        await app_state.sim_task
        
    return {"status": "ok", "run_id": app_state.engine.run_id}

@router.get("/simulation/status")
async def get_status(request: Request):
    app_state = request.app.state
    if not app_state.engine:
        return {"status": "stopped"}
    return app_state.engine.get_snapshot()

@router.get("/simulation/layout")
async def get_layout(request: Request):
    app_state = request.app.state
    if not app_state.engine:
        return {"status": "error", "message": "Simulation not running"}
    w = app_state.engine.warehouse
    return {
        "width": w.width,
        "height": w.height,
        "shelves": w.shelves,
        "induction_cells": w.induction_cells,
        "outbound_cells": w.outbound_cells,
    }

@router.get("/runs/{run_id}/analytics")
async def get_analytics(run_id: str, db: AsyncSession = Depends(get_db)):
    # Return placeholder if the db doesn't have it yet, we'll expand this later
    return await get_run_analytics(db, run_id)

@router.post("/simulation/interact/spill")
async def toggle_spill(x: int, y: int, request: Request):
    engine = request.app.state.engine
    if engine and engine.running:
        val = engine.warehouse.toggle_obstacle(x, y)
        return {"status": "ok", "obstacle_added": val}
    return {"status": "error", "message": "Sim not running"}
    
@router.post("/simulation/interact/task")
async def add_task(x: int, y: int, request: Request):
    engine = request.app.state.engine
    if engine and engine.running:
        if engine.warehouse.is_shelf(x, y):
            task = engine.scheduler.add_manual_task(x, y)
            return {"status": "ok", "task_id": task.id if task else None}
    return {"status": "error"}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == '{"type": "ping"}':
                await websocket.send_text('{"type": "pong"}')
    except WebSocketDisconnect:
        manager.disconnect(websocket)
