import random
import time
from collections import deque
from enum import Enum
from typing import List, Tuple, Dict, Any, Optional
from .warehouse import Warehouse
from .robot import Robot, RobotState
from .pathfinder import astar

class TaskStatus(Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    PICKED = "picked"
    DELIVERED = "delivered"
    FAILED = "failed"

class Task:
    def __init__(self, task_id: int, shelf_x: int, shelf_y: int, station_x: int, station_y: int, priority: int = 1):
        self.id = task_id
        self.shelf_x = shelf_x
        self.shelf_y = shelf_y
        self.station_x = station_x
        self.station_y = station_y
        self.priority = priority
        self.status = TaskStatus.PENDING
        self.created_at = time.time()
        self.picked_at: Optional[float] = None
        self.delivered_at: Optional[float] = None
        self.assigned_robot: Optional[int] = None

class TaskScheduler:
    def __init__(self, warehouse: Warehouse):
        self.warehouse = warehouse
        self.pending_tasks: deque = deque()
        self.active_tasks: Dict[int, Task] = {}
        self.next_task_id = 1
        
    def generate_tasks(self, count: int) -> List[Task]:
        new_tasks = []
        if not self.warehouse.shelves or not self.warehouse.outbound_cells:
            return []
            
        for _ in range(count):
            shelf = random.choice(self.warehouse.shelves)
            station = random.choice(self.warehouse.outbound_cells) # retrieval task targets outbound
            task = Task(self.next_task_id, shelf[0], shelf[1], station[0], station[1], random.randint(1, 3))
            self.next_task_id += 1
            self.pending_tasks.append(task)
            new_tasks.append(task)
            
        self._sort_pending()
        return new_tasks
        
    def add_manual_task(self, shelf_x: int, shelf_y: int) -> Optional[Task]:
        if not self.warehouse.outbound_cells:
            return None
        station = random.choice(self.warehouse.outbound_cells)
        task = Task(self.next_task_id, shelf_x, shelf_y, station[0], station[1], priority=3) # manual high priority
        self.next_task_id += 1
        self.pending_tasks.appendleft(task) # ensure it gets processed first
        return task
        
    def _sort_pending(self):
        sorted_tasks = sorted(self.pending_tasks, key=lambda t: t.priority, reverse=True)
        self.pending_tasks = deque(sorted_tasks)

    def get_adjacent_passable(self, x: int, y: int) -> Optional[Tuple[int,int]]:
        for nx, ny in self.warehouse.neighbors(x, y):
            if self.warehouse.is_passable(nx, ny):
                return (nx, ny)
        return None

    def assign_tasks(self, robots: List[Robot], warehouse: Warehouse) -> List[Tuple[Robot, Task, List[Tuple[int,int]]]]:
        assignments = []
        idle_robots = [r for r in robots if r.state == RobotState.IDLE]
        
        reserved = set()
        for r in robots:
            reserved.add((r.x, r.y))
            if r.path:
                reserved.add(r.path[0])
                
        for robot in idle_robots:
            if not self.pending_tasks:
                break
                
            task = self.pending_tasks.popleft()
            target_cell = self.get_adjacent_passable(task.shelf_x, task.shelf_y)
            
            if not target_cell:
                self.pending_tasks.append(task)
                continue
                
            if (robot.x, robot.y) in reserved:
                reserved.remove((robot.x, robot.y))
                
            path = astar(warehouse, (robot.x, robot.y), target_cell, reserved)
            reserved.add((robot.x, robot.y))
            
            if path is not None:
                task.status = TaskStatus.ASSIGNED
                task.assigned_robot = robot.id
                self.active_tasks[task.id] = task
                assignments.append((robot, task, path))
            else:
                self.pending_tasks.append(task)
                
        return assignments
