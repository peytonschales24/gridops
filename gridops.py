
from collections import deque

cardinal = [(0,1),(0,-1),(1,0),(-1,0)]
ordinal = [(-1,-1), (1,1), (-1,1), (1,-1)]
compass_rose=cardinal + ordinal

def gridbfs(grid,
            start_pos=(0,0),
            directions=cardinal,
            can_move_to=None,
            is_target=None):

    height = len(grid)
    width = len(grid[0])

    result = []

    distance = 0
    visited = set([start_pos])
    queue = [(start_pos,[])]
    while len(queue) != 0:
        newq = []
        
        for pos,path in queue:
            x,y=pos
            for dx, dy in directions:
                nx = x + dx
                ny = y + dy
                if nx < 0 or nx >= width:
                    continue
                if ny < 0 or ny >= height:
                    continue
                if not can_move_to(grid, ny, nx):
                    continue
                r = is_target(grid, ny, nx)
                if r is not None:
                    result.append((distance,path+[(ny,nx)],r))
                else:
                    if not (nx,ny) in visited:
                        visited.add((nx,ny))
                        newq.append(((nx, ny),path+[(y,x)]))
        if len(result) != 0:
            break
        queue = newq
        distance += 1

    return result

def griddfs(grid,
            start_pos=(0,0),
            directions=cardinal,
            can_move_to=None,
            is_target=None):

    q = deque()

    height = len(grid)
    width = len(grid[0])

    result = []

    q.append((start_pos,[]))
    while len(q) != 0:
        pos,path = q.pop()
        x,y=pos
        for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            if nx < 0 or nx >= width:
                continue
            if ny < 0 or ny >= height:
                continue
            if not can_move_to(grid, ny, nx):
                continue
            r = is_target(grid, ny, nx)
            if r is not None:
                result.append((path+[(ny,nx)],r))
            else:
                if not (ny,nx) in path:
                    q.append(((nx, ny),path+[(y,x)]))

    return result

def gridflood(grid, pos, newvalue, inplace=True):

    if not inplace:
        grid = grid.copy()

    start_value = grid[pos[0]][pos[1]]

    def cv(g,r,c):
        g[r][c] = newvalue
        return None
    
    gridbfs(grid, start_pos=pos,
            directions=cardinal,
            can_move_to=lambda g,r,c: g[r][c] == start_value,
            is_target=cv)
    return grid

if __name__ == '__main__':
    grid = [
        [0,0,0,0,0],
        [0,1,1,1,0],
        [0,1,2,1,0],
        [0,1,0,0,0],
        [0,0,1,1,1]
    ]

    r = gridbfs(grid, (0,0),
                can_move_to=lambda g,r,c: grid[r][c] != 1,
                is_target=lambda g,r,c: True if grid[r][c] == 2 else None)

    print(r)


    grid = [
        [0,0,0,0,0],
        [0,1,1,1,0],
        [0,1,0,0,0],
        [0,1,1,1,0],
        [0,0,0,0,1]
    ]

    g = gridflood(grid, (0,0), 2)
    for r in g:
        print(r)

