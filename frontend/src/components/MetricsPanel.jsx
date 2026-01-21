import React from 'react';
import useSimStore from '../store/useSimStore';

export default function MetricsPanel() {
  const { metrics, tick, simTime } = useSimStore();

  return (
    <div className="flex flex-col gap-4 p-4 border border-slate-700 rounded-md bg-bg-secondary h-full">
      <h2 className="text-xl font-bold border-b border-slate-700 pb-2">Metrics & Stats</h2>
      <div className="grid grid-cols-2 gap-4 text-sm">
        <div className="p-3 bg-bg-tertiary rounded">
          <p className="text-slate-400">Total Ticks</p>
          <p className="text-2xl font-mono">{tick}</p>
        </div>
        <div className="p-3 bg-bg-tertiary rounded">
          <p className="text-slate-400">Sim Time</p>
          <p className="text-2xl font-mono">{simTime.toFixed(1)}s</p>
        </div>
        <div className="p-3 bg-bg-tertiary rounded">
          <p className="text-slate-400">Active Robots</p>
          <p className="text-2xl font-mono text-accent-blue">{metrics.active_robots || 0}</p>
        </div>
        <div className="p-3 bg-bg-tertiary rounded">
          <p className="text-slate-400">Pending Tasks</p>
          <p className="text-2xl font-mono text-accent-teal">{metrics.tasks_pending || 0}</p>
        </div>
      </div>
    </div>
  );
}
