import heapq
from typing import Optional, List, Tuple, Set
from .warehouse import Warehouse

def heuristic(a: Tuple[int,int], b: Tuple[int,int]) -> int:
    """Manhattan distance."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(
    warehouse: Warehouse,
    start: Tuple[int,int],
    goal: Tuple[int,int],
    reserved: Optional[Set[Tuple[int,int]]] = None
) -> Optional[List[Tuple[int,int]]]:
    """
    Returns ordered list of (x,y) cells from start to goal (inclusive),
    or None if no path exists.
    """
    reserved = reserved or set()
    
    # The goal must be passable (or we're already there)
    if not warehouse.is_passable(goal[0], goal[1]) and start != goal:
        return None

    open_set = []
    heapq.heappush(open_set, (0, 0, start))
    
    came_from = {}
    
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    
    while open_set:
        _, current_g, current = heapq.heappop(open_set)
        
        if current == goal:
            # Reconstruct path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path
            
        # Optimization: since we use a heap, we might pop an old worse state
        if current_g > g_score.get(current, float('inf')):
            continue
            
        for neighbor in warehouse.neighbors(current[0], current[1]):
            # Treat reserved cells as impassable
            if neighbor in reserved and neighbor != goal:
                continue
                
            tentative_g_score = g_score[current] + 1
            
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f = tentative_g_score + heuristic(neighbor, goal)
                f_score[neighbor] = f
                heapq.heappush(open_set, (f, tentative_g_score, neighbor))
                
    return None
