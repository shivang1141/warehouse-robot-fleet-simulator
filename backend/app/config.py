from pydantic import BaseModel

class SimConfig(BaseModel):
    grid_width: int = 30
    grid_height: int = 20
    robot_count: int = 12
    tick_rate_hz: float = 4.0          # ticks per second
    initial_tasks: int = 20
    task_replenish_threshold: int = 5  # add tasks when queue drops below this
    task_replenish_count: int = 10
    pick_delay_ticks: int = 3
    highway_width: int = 2             # Symbotic highway lanes
