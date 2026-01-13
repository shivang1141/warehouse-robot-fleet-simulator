from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

async def get_run_analytics(session: AsyncSession, run_id: str):
    analytics = {}
    
    # Avg delivery time
    avg_delivery_stmt = text("""
    SELECT AVG(delivered_at - created_at) as avg_delivery_secs
    FROM tasks WHERE run_id = :run_id AND status = 'delivered'
    """)
    res = await session.execute(avg_delivery_stmt, {"run_id": run_id})
    row = res.fetchone()
    analytics["avg_delivery_time_secs"] = row[0] if row and row[0] is not None else 0.0
    
    # Throughput per min using rough approximation (SQLite valid)
    throughput_stmt = text("""
    SELECT 
      CAST((timestamp / 60) AS INTEGER) as minute_bucket,
      COUNT(*) as deliveries
    FROM robot_events
    WHERE run_id = :run_id AND event_type = 'deliver'
    GROUP BY CAST((timestamp / 60) AS INTEGER)
    ORDER BY minute_bucket
    """)
    res = await session.execute(throughput_stmt, {"run_id": run_id})
    buckets = [r[1] for r in res.fetchall()]
    analytics["throughput_per_min"] = sum(buckets) / len(buckets) if buckets else 0.0
    
    # Robot stats
    robot_stmt = text("""
    SELECT
      robot_id,
      SUM(CASE WHEN event_type = 'deliver' THEN 1 ELSE 0 END) as tasks_completed,
      SUM(CASE WHEN event_type = 'move' THEN 1 ELSE 0 END) as steps_taken,
      SUM(CASE WHEN event_type = 'error' THEN 1 ELSE 0 END) as error_count
    FROM robot_events
    WHERE run_id = :run_id
    GROUP BY robot_id
    ORDER BY robot_id
    """)
    res = await session.execute(robot_stmt, {"run_id": run_id})
    analytics["robot_stats"] = [
        {"robot_id": r[0], "tasks_completed": r[1], "steps_taken": r[2], "error_count": r[3]}
        for r in res.fetchall()
    ]
    
    return analytics
