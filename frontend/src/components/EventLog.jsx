import React from 'react';
import useSimStore from '../store/useSimStore';

export default function EventLog() {
  const { events } = useSimStore();

  return (
    <div className="flex flex-col gap-2 p-4 border border-slate-700 rounded-md bg-bg-secondary h-full overflow-hidden">
      <h2 className="text-xl font-bold border-b border-slate-700 pb-2">Event Feed</h2>
      <div className="overflow-y-auto flex-grow pr-2">
        {events.length === 0 ? (
          <p className="text-slate-500 text-sm mt-4 text-center">No events yet...</p>
        ) : (
          <ul className="space-y-2">
            {events.map((ev, i) => (
              <li key={i} className="text-xs font-mono p-2 bg-bg-tertiary rounded flex gap-2 border-l-2 border-slate-600">
                <span className="text-slate-400">[{ev.sim_time?.toFixed(1) || 0}s]</span>
                <span className="font-bold text-accent-blue">R{ev.robot_id}</span>
                <span className={`px-1 rounded ${ev.event_type === 'pick' ? 'bg-accent-amber/20 text-yellow-500' : ev.event_type === 'deliver' ? 'bg-accent-teal/20 text-emerald-400' : 'text-slate-300'}`}>
                  {ev.event_type.toUpperCase()}
                </span>
                {ev.detail?.task_id && <span className="text-slate-400">Task:{ev.detail.task_id}</span>}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
