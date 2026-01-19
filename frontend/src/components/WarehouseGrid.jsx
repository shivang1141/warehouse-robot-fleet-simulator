import React, { useRef, useEffect, useState } from 'react';
import useSimStore from '../store/useSimStore';
import axios from 'axios';

const CELL_COLORS = {
  EMPTY: '#1a1d27',     // dark card bg
  SHELF: '#1e3a8a',     // deep blue for dense matrix
  INDUCTION: '#22c55e', // bright green
  OUTBOUND: '#0d9488',  // teal
  OBSTACLE: '#b91c1c'   // red spill
};

const ROBOT_COLORS = {
  idle:       '#475569', // slate-600
  moving:     '#3b82f6', // blue-500
  picking:    '#f59e0b', // amber-500
  delivering: '#10b981', // emerald-500
  error:      '#ef4444', // red-500
};

export default function WarehouseGrid() {
  const canvasRef = useRef(null);
  const { robots, obstacles, simConfig } = useSimStore();
  const [layout, setLayout] = useState(null);
  
  const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

  useEffect(() => {
    axios.get(`${apiBase}/simulation/layout`)
      .then(res => {
        if(res.data.status !== 'error') {
          setLayout(res.data);
        }
      })
      .catch(err => console.log('Layout not ready or sim not started'));
  }, [apiBase, robots.length]); // refetch when robots update incase layout changed from stop/start

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    
    // Read actual size
    const parent = canvas.parentElement;
    canvas.width = parent.clientWidth;
    canvas.height = parent.clientHeight;
    
    const { grid_width, grid_height } = simConfig;
    const cw = canvas.width;
    const ch = canvas.height;
    
    const cellSize = Math.min(cw / grid_width, ch / grid_height);
    const offsetX = (cw - (grid_width * cellSize)) / 2;
    const offsetY = (ch - (grid_height * cellSize)) / 2;

    const render = () => {
      ctx.fillStyle = '#0f1117'; 
      ctx.fillRect(0, 0, cw, ch);
      
      for (let y = 0; y < grid_height; y++) {
        for (let x = 0; x < grid_width; x++) {
          ctx.fillStyle = CELL_COLORS.EMPTY;
          ctx.fillRect(offsetX + x * cellSize, offsetY + y * cellSize, cellSize - 1, cellSize - 1);
        }
      }
      
      if (layout) {
        layout.shelves.forEach(([x, y]) => {
          ctx.fillStyle = CELL_COLORS.SHELF;
          ctx.fillRect(offsetX + x * cellSize, offsetY + y * cellSize, cellSize - 1, cellSize - 1);
        });
        layout.induction_cells.forEach(([x, y]) => {
          ctx.fillStyle = CELL_COLORS.INDUCTION;
          ctx.fillRect(offsetX + x * cellSize, offsetY + y * cellSize, cellSize - 1, cellSize - 1);
        });
        layout.outbound_cells.forEach(([x, y]) => {
          ctx.fillStyle = CELL_COLORS.OUTBOUND;
          ctx.fillRect(offsetX + x * cellSize, offsetY + y * cellSize, cellSize - 1, cellSize - 1);
        });
      }
      
      obstacles.forEach(([x, y]) => {
        ctx.fillStyle = CELL_COLORS.OBSTACLE;
        ctx.fillRect(offsetX + x * cellSize, offsetY + y * cellSize, cellSize - 1, cellSize - 1);
      });
      
      robots.forEach(r => {
        const cx = offsetX + r.x * cellSize + cellSize / 2;
        const cy = offsetY + r.y * cellSize + cellSize / 2;
        const radius = (cellSize / 2) * 0.7;
        
        ctx.beginPath();
        ctx.arc(cx, cy, radius, 0, 2 * Math.PI);
        ctx.fillStyle = ROBOT_COLORS[r.state] || ROBOT_COLORS.idle;
        ctx.fill();
        
        if (r.carrying) {
          ctx.beginPath();
          ctx.arc(cx, cy, radius * 0.4, 0, 2 * Math.PI);
          ctx.fillStyle = '#10b981';
          ctx.fill();
        }
        
        ctx.fillStyle = '#fff';
        ctx.font = `bold ${Math.max(10, radius * 0.8)}px sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(r.id, cx, cy);
      });
    };
    
    render();
    
    const onResize = () => render();
    window.addEventListener('resize', onResize);
    
    return () => {
      window.removeEventListener('resize', onResize);
    };
  }, [robots, obstacles, layout, simConfig]);

  const handleCanvasClick = async (e) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const { grid_width, grid_height } = simConfig;
    const cw = canvas.width;
    const ch = canvas.height;
    const cellSize = Math.min(cw / grid_width, ch / grid_height);
    const offsetX = (cw - (grid_width * cellSize)) / 2;
    const offsetY = (ch - (grid_height * cellSize)) / 2;
    
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    
    const gx = Math.floor((mx - offsetX) / cellSize);
    const gy = Math.floor((my - offsetY) / cellSize);
    
    if (gx >= 0 && gx < grid_width && gy >= 0 && gy < grid_height) {
      const isShelf = layout?.shelves?.some(([x,y]) => x === gx && y === gy);
      if (isShelf) {
        await axios.post(`${apiBase}/simulation/interact/task?x=${gx}&y=${gy}`);
      } else {
        await axios.post(`${apiBase}/simulation/interact/spill?x=${gx}&y=${gy}`);
      }
    }
  };

  return (
    <div className="w-full h-full min-h-[400px] flex-grow relative bg-bg-primary overflow-hidden border border-slate-700 rounded-md">
      <canvas 
        ref={canvasRef} 
        style={{ width: '100%', height: '100%', cursor: 'crosshair', display: 'block' }} 
        onClick={handleCanvasClick}
      />
    </div>
  );
}
