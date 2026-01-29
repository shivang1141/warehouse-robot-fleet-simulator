# Symbotic Warehouse Robot Fleet Simulator

A high-performance, real-time 2D simulation of a Symbotic-inspired automated warehouse. The application features a densely packed storage matrix, high-speed transit pathways, and autonomous robotic swarms processing dynamic induction and retrieval tasks.

## Architecture

1.  **FastAPI Backend (Python 3.11)**: Orchestrates the core simulation physics, A* dynamic pathfinding, and Websocket event streaming.
2.  **React Frontend (React 18 + Zustand + Canvas)**: Renders the swarm in real-time. Employs HTML5 Canvas optimized for 60FPS fluid movements with low memory footprint.
3.  **Persistence Layer (SQLite + SQLAlchemy)**: Silently logs every robotic maneuver into a persistent datastore, empowering analytics and future historical playbacks.

## Tech Stack

| Layer          | Technology                                   |
| -------------- | ------------------------------------- |
| **Backend**    | FastAPI, Pydantic, SQLAlchemy 2.0 (async), WebSockets |
| **Frontend**   | React 18, Vite, Zustand, Tailwind CSS, Recharts |
| **Persistence**| SQLite (via aiosqlite, MS SQL compatible)   |
| **DevOps**     | Docker, Docker Compose, GitHub Actions |

## Quick Start

The entire stack is packaged and ready to run locally:

```bash
# 1. Clone the repository
git clone <your-repo-url>

# 2. Boot the full application via Docker
make dev

# 3. Access the dashboard
# Open your browser to http://localhost:5173
```

## API Reference

- `POST /simulation/start`: Boots the engine and assigns the initial queue.
- `POST /simulation/stop`: Gracefully powers down the current run.
- `GET /simulation/layout`: Returns the static grid definitions (shelves, stations).
- `GET /simulation/status`: Grabs the explicit tick snapshot without WS connection.
- `GET /runs/{run_id}/analytics`: Performs SQL aggregation parsing throughput metrics.

*Interactive Elements:*
- `POST /simulation/interact/spill?x={x}&y={y}`: Dynamically inserts an impassible obstacle.
- `POST /simulation/interact/task?x={x}&y={y}`: Queues an immediate high-priority retrieval task.

## How It Works

- **Symbotic Storage Matrix**: Designed exactly like Symbotic systems, dense cores of shelves are surrounded by unbroken exterior highway paths.
- **A* Pathfinding**: The system dynamically avoids collisions by injecting active robot coordinates as temporary blockages alongside user-generated spills.
- **WebSocket Ticking**: The REST backend functions asynchronously, ticking the physical simulation loop forward rapidly while simultaneously streaming JSON snapshots to Vite.

## Running Tests

Execute the unit test suites on the pathfinding heuristics and FastAPI routes:
```bash
make test
```

## Resume Highlights
- **Engineered a real-time Symbotic-style warehouse fleet simulator** using python asyncio and FastAPI WebSockets, managing A* pathfinding and collision avoidance for massive robot swarms.
- **Built an ultra-fast HTML5 Canvas visualization dashboard** with React and Zustand, offering sub-second interactivity and rendering for dense layout structures.
- **Implemented zero-blocking analytics infrastructure** buffering thousands of robotic telemetry events per minute and asynchronously committing them to a SQL database.
