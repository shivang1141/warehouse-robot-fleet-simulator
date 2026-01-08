import asyncio
import uuid
import random
from typing import Callable, Any, List
from ..config import SimConfig
from .warehouse import Warehouse
from .robot import Robot, RobotState
from .scheduler import TaskScheduler
from .pathfinder import astar

class SimulationEngine:
    def __init__(self, config: SimConfig, db_session: Any, broadcast_fn: Callable):
        self.config = config
        self.db = db_session
        self.broadcast = broadcast_fn
        self.warehouse = Warehouse(config.grid_width, config.grid_height)
        self.robots: List[Robot] = []
        self.scheduler = TaskScheduler(self.warehouse)
        self.run_id: str = str(uuid.uuid4())
        self.tick: int = 0
        self.running: bool = False
        self.sim_time: float = 0.0
        self.event_buffer: List[dict] = []

    async def start(self):
        self.warehouse.generate_layout()
        
        # Place robots at random empty cells
        empty_cells = []
        for y in range(self.warehouse.height):
            for x in range(self.warehouse.width):
                if self.warehouse.is_passable(x, y):
                    empty_cells.append((x, y))
                    
        random.shuffle(empty_cells)
        
        for i in range(self.config.robot_count):
            if not empty_cells:
                break
            x, y = empty_cells.pop()
            self.robots.append(Robot(i + 1, x, y))
            
        self.scheduler.generate_tasks(self.config.initial_tasks)
        
        # We will save the simulation run to the DB in Phase 2
        
        self.running = True
        tick_interval = 1.0 / self.config.tick_rate_hz
        
        while self.running:
            await self._tick()
            await asyncio.sleep(tick_interval)

    async def _tick(self):
        # 1. Assign tasks
        assignments = self.scheduler.assign_tasks(self.robots, self.warehouse)
        for robot, task, path in assignments:
            robot.assign_task(task, path)
            
        # 2. Step robots
        for robot in self.robots:
            event = robot.step(self.config.pick_delay_ticks)
            if event:
                ev_type, ev_data = event
                # Record event
                ev_record = {
                    "run_id": self.run_id,
                    "robot_id": robot.id,
                    "timestamp": self.sim_time,
                    "event_type": ev_type,
                    "detail": ev_data
                }
                self.event_buffer.append(ev_record)
                
                # Handling DELIVERING transition explicitly
                if ev_type == "pick" and robot.current_task:
                    target = self.scheduler.get_adjacent_passable(robot.current_task.station_x, robot.current_task.station_y)
                    if target:
                        reserved = { (r.x, r.y) for r in self.robots }
                        if (robot.x, robot.y) in reserved:
                            reserved.remove((robot.x, robot.y))
                        new_path = astar(self.warehouse, (robot.x, robot.y), target, reserved)
                        if new_path is not None:
                            robot.path = new_path
                            if robot.path and robot.path[0] == (robot.x, robot.y):
                                robot.path.pop(0)
                        else:
                            robot.state = RobotState.ERROR

        # 3. Replenish tasks
        if len(self.scheduler.pending_tasks) < self.config.task_replenish_threshold:
            self.scheduler.generate_tasks(self.config.task_replenish_count)
            
        # 4. Flush events to DB (placeholder until Phase 2)
        if self.tick > 0 and self.tick % 10 == 0 and self.event_buffer:
            self.event_buffer.clear()
            
        # 5. Broadcast snapshot
        snapshot = self.get_snapshot()
        await self.broadcast(snapshot)
        
        self.tick += 1
        self.sim_time += (1.0 / self.config.tick_rate_hz)

    def get_snapshot(self) -> dict:
        return {
            "type": "snapshot",
            "run_id": self.run_id,
            "tick": self.tick,
            "sim_time": self.sim_time,
            "robots": [
                {
                    "id": r.id, "x": r.x, "y": r.y, 
                    "state": r.state.value, "carrying": r.carrying_item
                } for r in self.robots
            ],
            "metrics": {
                "active_robots": sum(1 for r in self.robots if r.state != RobotState.IDLE),
                "idle_robots": sum(1 for r in self.robots if r.state == RobotState.IDLE),
                "tasks_pending": len(self.scheduler.pending_tasks),
            },
            "obstacles": list(self.warehouse.obstacles)
        }

    async def stop(self):
        self.running = False
