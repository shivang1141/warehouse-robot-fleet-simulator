from enum import Enum
from typing import Optional, List, Tuple, Any

class RobotState(Enum):
    IDLE       = "idle"
    MOVING     = "moving"
    PICKING    = "picking"
    DELIVERING = "delivering"
    ERROR      = "error"

class Robot:
    def __init__(self, robot_id: int, x: int, y: int):
        self.id = robot_id
        self.x = x
        self.y = y
        self.state: RobotState = RobotState.IDLE
        self.current_task: Any = None
        self.path: List[Tuple[int,int]] = []
        self.carrying_item: bool = False
        self.tasks_completed: int = 0
        self.steps_taken: int = 0
        self.error_count: int = 0
        self.wait_ticks: int = 0

    def assign_task(self, task: Any, path: List[Tuple[int,int]]) -> None:
        self.current_task = task
        self.path = list(path)
        if self.path and self.path[0] == (self.x, self.y):
            self.path.pop(0)
        self.state = RobotState.MOVING
        
    def step(self, pick_delay: int) -> Optional[Tuple[str, dict]]:
        if self.state in (RobotState.IDLE, RobotState.ERROR):
            return None
            
        if self.state == RobotState.PICKING:
            if self.wait_ticks > 0:
                self.wait_ticks -= 1
                return None
            else:
                self.carrying_item = True
                self.state = RobotState.DELIVERING
                # Note: engine/scheduler will assign the next path to outbound station here
                return ("pick", {"task_id": getattr(self.current_task, "id", None)})
                
        if self.state in (RobotState.MOVING, RobotState.DELIVERING):
            if not self.path:
                # Reached the end of the path
                if self.state == RobotState.MOVING:
                    self.state = RobotState.PICKING
                    self.wait_ticks = pick_delay
                    return None
                elif self.state == RobotState.DELIVERING:
                    self.state = RobotState.IDLE
                    self.carrying_item = False
                    self.tasks_completed += 1
                    t_id = getattr(self.current_task, "id", None)
                    return ("deliver", {"task_id": t_id})
            
            # Step forward
            next_step = self.path.pop(0)
            from_x, from_y = self.x, self.y
            self.x, self.y = next_step
            self.steps_taken += 1
            return ("move", {
                "from_x": from_x, "from_y": from_y,
                "to_x": self.x, "to_y": self.y,
                "task_id": getattr(self.current_task, "id", None)
            })
            
        return None
