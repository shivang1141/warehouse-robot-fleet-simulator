import React from 'react';
import SimControls from './components/SimControls';
import WarehouseGrid from './components/WarehouseGrid';
import MetricsPanel from './components/MetricsPanel';
import EventLog from './components/EventLog';
import { useWebSocket } from './hooks/useWebSocket';

function App() {
  const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';
  useWebSocket(wsUrl);

  return (
    <div className="h-screen w-screen flex flex-col bg-bg-primary text-slate-100 overflow-hidden font-sans">
      <SimControls />
      <div className="flex-grow flex flex-col md:flex-row p-4 gap-4 h-[calc(100vh-80px)]">
        <div className="flex-[3]">
          <WarehouseGrid />
        </div>
        <div className="flex-1 flex flex-col gap-4 min-w-[300px]">
          <div className="flex-1">
            <MetricsPanel />
          </div>
          <div className="flex-[3] overflow-hidden">
            <EventLog />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
