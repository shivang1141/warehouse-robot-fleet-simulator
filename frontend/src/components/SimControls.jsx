import React from 'react';
import useSimStore from '../store/useSimStore';
import axios from 'axios';

export default function SimControls() {
  const { wsConnected, runId } = useSimStore();
  const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

  const startSim = () => axios.post(`${apiBase}/simulation/start`);
  const stopSim = () => axios.post(`${apiBase}/simulation/stop`);

  return (
    <div className="flex items-center justify-between p-4 bg-bg-secondary border-b border-slate-700">
      <div className="flex items-center gap-4">
        <h1 className="text-2xl font-bold bg-gradient-to-r from-accent-blue to-accent-teal bg-clip-text text-transparent">
          Symbotic Fleet Simulator
        </h1>
        <div className="flex items-center gap-2 text-sm">
          <span className={`w-3 h-3 rounded-full ${wsConnected ? 'bg-green-500 shadow-[0_0_8px_#22c55e]' : 'bg-red-500 shadow-[0_0_8px_#ef4444]'}`}></span>
          <span className="text-slate-400">{wsConnected ? 'Connected (Live)' : 'Disconnected'}</span>
        </div>
      </div>
      
      <div className="flex gap-4 items-center">
        {runId && <span className="font-mono text-sm text-slate-400">Run: {runId.substring(0,8)}</span>}
        <button onClick={startSim} className="px-4 py-2 bg-accent-blue hover:bg-blue-600 rounded text-white font-medium transition-colors">
          Start Sim
        </button>
        <button onClick={stopSim} className="px-4 py-2 bg-slate-700 hover:bg-red-500 rounded text-white font-medium transition-colors">
          Stop
        </button>
      </div>
    </div>
  );
}
