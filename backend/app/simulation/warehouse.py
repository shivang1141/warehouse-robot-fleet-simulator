EMPTY = 0
SHELF = 1
INDUCTION = 2
WALL = 3
OUTBOUND = 4
OBSTACLE = 5

class Warehouse:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[EMPTY for _ in range(width)] for _ in range(height)]
        self.shelves: list[tuple[int,int]] = []
        self.induction_cells: list[tuple[int,int]] = []
        self.outbound_cells: list[tuple[int,int]] = []
        self.obstacles: set[tuple[int,int]] = set()
        
    def generate_layout(self):
        """
        Symbotic-inspired Layout:
        - Leftmost column (x=0) used for Induction cells.
        - Rightmost column (x=width-1) used for Outbound cells.
        - Top/Bottom/Sides are high-speed highways.
        - Dense internal blocks of shelves separated by narrow vertical aisles.
        """
        # Create Induction & Outbound
        for y in range(2, self.height - 2, 2):
            self.grid[y][0] = INDUCTION
            self.induction_cells.append((0, y))
            
            self.grid[y][self.width - 1] = OUTBOUND
            self.outbound_cells.append((self.width - 1, y))
            
        # Create Dense Storage Matrix
        # Leave columns 1, 2 for induction highway
        # Leave columns width-2, width-3 for outbound highway
        # Leave rows 0, 1 and height-1, height-2 for top/bottom highways
        
        for y in range(2, self.height - 2):
            for x in range(3, self.width - 3):
                # Vertical aisles every 5 columns
                if x % 5 == 0:
                    continue
                # Horizontal aisles every 4 rows
                if y % 4 == 0:
                    continue
                
                self.grid[y][x] = SHELF
                self.shelves.append((x, y))

    def is_passable(self, x: int, y: int) -> bool:
        """Returns True if a robot can occupy this cell."""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        # Obstacles (spills) block passage dynamically
        if (x, y) in self.obstacles:
            return False
        return self.grid[y][x] in (EMPTY, INDUCTION, OUTBOUND)

    def is_shelf(self, x: int, y: int) -> bool:
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.grid[y][x] == SHELF

    def neighbors(self, x: int, y: int) -> list[tuple[int,int]]:
        """4-directional passable neighbors (no diagonals)."""
        dirs = [(-1,0), (1,0), (0,-1), (0,1)]
        res = []
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if self.is_passable(nx, ny):
                res.append((nx, ny))
        return res
        
    def toggle_obstacle(self, x: int, y: int) -> bool:
        """User interaction: toggle dynamic obstacle (spill) on an empty cell"""
        if 0 <= x < self.width and 0 <= y < self.height:
            if self.grid[y][x] == EMPTY:
                pt = (x, y)
                if pt in self.obstacles:
                    self.obstacles.remove(pt)
                    return False
                else:
                    self.obstacles.add(pt)
                    return True
        return False
