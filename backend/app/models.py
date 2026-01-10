from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class RobotEvent(Base):
    __tablename__ = "robot_events"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String, index=True, nullable=False)
    robot_id = Column(Integer, index=True, nullable=False)
    timestamp = Column(Float, nullable=False)
    wall_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    event_type = Column(String, nullable=False)
    from_x = Column(Integer, nullable=True)
    from_y = Column(Integer, nullable=True)
    to_x = Column(Integer, nullable=True)
    to_y = Column(Integer, nullable=True)
    task_id = Column(Integer, nullable=True)
    detail = Column(Text, nullable=True)

class TaskRecord(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String, index=True, nullable=False)
    assigned_robot = Column(Integer, nullable=True)
    shelf_x = Column(Integer, nullable=False)
    shelf_y = Column(Integer, nullable=False)
    station_x = Column(Integer, nullable=False)
    station_y = Column(Integer, nullable=False)
    created_at = Column(Float, nullable=False)
    picked_at = Column(Float, nullable=True)
    delivered_at = Column(Float, nullable=True)
    status = Column(String, default='pending', nullable=False)
    priority = Column(Integer, default=1, nullable=False)

class SimulationRun(Base):
    __tablename__ = "simulation_runs"
    
    run_id = Column(String, primary_key=True)
    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    robot_count = Column(Integer, nullable=False)
    grid_width = Column(Integer, nullable=False)
    grid_height = Column(Integer, nullable=False)
    total_tasks = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
