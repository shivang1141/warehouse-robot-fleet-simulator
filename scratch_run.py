import asyncio
import sys
import os
sys.path.append(os.path.abspath('.'))

from backend.app.config import SimConfig
from backend.app.simulation.engine import SimulationEngine

async def test_broadcast(snapshot):
    print(f"Tick {snapshot['tick']}: {snapshot['metrics']['active_robots']} active robots, {len(snapshot['obstacles'])} obstacles.")
    for r in snapshot['robots'][:2]:
        print(f"  Robot {r['id']}: {r['state']} at ({r['x']}, {r['y']})")
    print()

async def main():
    config = SimConfig()
    engine = SimulationEngine(config, None, test_broadcast)
    
    # Run in background
    task = asyncio.create_task(engine.start())
    
    # Let it run for a bit
    await asyncio.sleep(2)
    
    # Stop
    await engine.stop()
    await task
    
if __name__ == "__main__":
    asyncio.run(main())
