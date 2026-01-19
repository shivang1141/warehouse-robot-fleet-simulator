import { useEffect } from 'react';
import useSimStore from '../store/useSimStore';

export function useWebSocket(url) {
  const applySnapshot = useSimStore(s => s.applySnapshot);
  const pushEvent = useSimStore(s => s.pushEvent);
  const setConnected = useSimStore(s => s.setWsConnected);

  useEffect(() => {
    let ws = null;
    let reconnectTimer = null;

    const connect = () => {
      ws = new WebSocket(url);
      
      ws.onopen = () => {
        setConnected(true);
      };
      
      ws.onclose = () => {
        setConnected(false);
        reconnectTimer = setTimeout(connect, 2000);
      };
      
      ws.onmessage = (e) => {
        try {
          const msg = JSON.parse(e.data);
          if (msg.type === 'snapshot') applySnapshot(msg);
          if (msg.type === 'event') pushEvent(msg);
        } catch (error) {
          console.error("WS Parse error", error);
        }
      };
    };

    connect();

    return () => {
      if (reconnectTimer) clearTimeout(reconnectTimer);
      if (ws) {
        ws.onclose = null;
        ws.close();
      }
    };
  }, [url, applySnapshot, pushEvent, setConnected]);
}
