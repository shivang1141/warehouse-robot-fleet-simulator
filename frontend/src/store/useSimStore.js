import { create } from 'zustand'

const useSimStore = create((set, get) => ({
  wsConnected: false,
  setWsConnected: (v) => set({ wsConnected: v }),

  runId: null,
  tick: 0,
  simTime: 0,
  robots: [],
  metrics: {},
  events: [],
  obstacles: [],

  playbackRunId: null,
  playbackTick: 0,
  playbackMaxTick: 0,
  playbackData: [],
  isPlaying: false,

  simConfig: { grid_width: 30, grid_height: 20, robot_count: 12 },
  simRunning: false,

  applySnapshot: (snap) => set({
    robots: snap.robots,
    metrics: snap.metrics,
    tick: snap.tick,
    runId: snap.run_id,
    simTime: snap.sim_time,
    obstacles: snap.obstacles || []
  }),
  
  pushEvent: (ev) => set((s) => ({ events: [ev, ...s.events].slice(0, 50) })),
  
  setPlaybackRun: (runId, events, maxTick) => set({
    playbackRunId: runId, playbackData: events, playbackMaxTick: maxTick
  }),
  setPlaybackTick: (t) => set({ playbackTick: t }),
}));

export default useSimStore;
