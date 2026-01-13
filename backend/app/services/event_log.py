import json
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import RobotEvent

async def batch_insert_events(session: AsyncSession, events_data: list[dict]):
    if not events_data:
        return
        
    for data in events_data:
        ev = RobotEvent(
            run_id=data["run_id"],
            robot_id=data["robot_id"],
            timestamp=data["timestamp"],
            event_type=data["event_type"],
            from_x=data.get("detail", {}).get("from_x"),
            from_y=data.get("detail", {}).get("from_y"),
            to_x=data.get("detail", {}).get("to_x"),
            to_y=data.get("detail", {}).get("to_y"),
            task_id=data.get("detail", {}).get("task_id"),
            detail=json.dumps(data.get("detail", {}))
        )
        session.add(ev)
        
    await session.commit()
