import pygame
from queue import PriorityQueue
from collections import deque

pygame.init()

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH + 40))
pygame.display.set_caption("Pathfinding Visualizer")

# Define colors
COLOURS = {
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "PURPLE": (128, 0, 128),
    "ORANGE": (255, 165, 0),
    "GRAY": (128, 128, 128),
    "TURQUOISE": (64, 224, 208),
    "NEGATIVE": (100, 100, 255)
}

FONT = pygame.font.SysFont("Arial", 20)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width + 40
        self.color = COLOURS["WHITE"]
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.negative_weight = False

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == COLOURS["RED"]

    def is_open(self):
        return self.color == COLOURS["GREEN"]

    def is_barrier(self):
        return self.color == COLOURS["BLACK"]

    def is_start(self):
        return self.color == COLOURS["ORANGE"]

    def is_end(self):
        return self.color == COLOURS["TURQUOISE"]

    def reset(self):
        self.color = COLOURS["WHITE"]
        self.negative_weight = False

    def make_start(self):
        self.color = COLOURS["ORANGE"]

    def make_closed(self):
        self.color = COLOURS["RED"]

    def make_open(self):
        self.color = COLOURS["GREEN"]

    def make_barrier(self):
        self.color = COLOURS["BLACK"]

    def make_end(self):
        self.color = COLOURS["TURQUOISE"]

    def make_path(self):
        self.color = COLOURS["PURPLE"]

    def make_negative(self):
        self.color = COLOURS["NEGATIVE"]
        self.negative_weight = True

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def draw_header(win, selected_algorithm):
    pygame.draw.rect(win, COLOURS["GRAY"], (0, 0, WIDTH, 40))
    text = FONT.render(f"Algorithm: {selected_algorithm} (1-4), N: Neg Weights (FW), SPACE: Run, C: Clear", True, COLOURS["WHITE"])
    win.blit(text, (10, 10))


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, COLOURS["GRAY"], (0, i * gap + 40), (width, i * gap + 40))
        for j in range(rows):
            pygame.draw.line(win, COLOURS["GRAY"], (j * gap, 40), (j * gap, width + 40))


def draw(win, grid, rows, width, selected_algorithm):
    win.fill(COLOURS["WHITE"])
    draw_header(win, selected_algorithm)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            grid[i].append(Node(i, j, gap, rows))
    return grid


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x, y = pos
    row = (y - 40) // gap
    col = x // gap
    return row, col


def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(prev, current, draw):
    while current in prev and prev[current] is not None:
        current = prev[current]
        current.make_path()
        draw()



def bfs(draw, grid, start, end):
    queue = deque([start])
    came_from = {start: None}
    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = queue.popleft()
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
        for neighbor in current.neighbors:
            if neighbor not in came_from and not neighbor.is_barrier():
                queue.append(neighbor)
                came_from[neighbor] = current
                neighbor.make_open()
        draw()
        if current != start:
            current.make_closed()
    return False


def dijkstra(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    dist = {node: float("inf") for row in grid for node in row}
    dist[start] = 0
    open_set_hash = {start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end:
            reconstruct_path(came_from, current, draw)
            end.make_end()
            start.make_start()
            return True
        for neighbor in current.neighbors:
            weight = 1
            if dist[current] + weight < dist[neighbor]:
                dist[neighbor] = dist[current] + weight
                came_from[neighbor] = current
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((dist[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
        if current != start:
            current.make_closed()
    return False


def astar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    f_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score[start] = heuristic(start.get_pos(), end.get_pos())
    open_set_hash = {start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end:
            reconstruct_path(came_from, current, draw)
            end.make_end()
            start.make_start()
            return True
        for neighbor in current.neighbors:
            temp_g = g_score[current] + 1
            if temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
        if current != start:
            current.make_closed()
    return False

def bellman_ford(draw, grid, start, end):
    nodes = [node for row in grid for node in row]
    edges = []

    for node in nodes:
        for neighbor in node.neighbors:
            weight = -1 if neighbor.negative_weight else 1
            edges.append((node, neighbor, weight))

    distance = {node: float("inf") for node in nodes}
    predecessor = {node: None for node in nodes}
    distance[start] = 0

    for _ in range(len(nodes) - 1):
        for u, v, w in edges:
            if distance[u] + w < distance[v]:
                distance[v] = distance[u] + w
                predecessor[v] = u

    # Negative cycle check (optional, just prints warning)
    for u, v, w in edges:
        if distance[u] + w < distance[v]:
            print("Warning: Negative weight cycle detected!")
            break

    # Path reconstruction
    current = end
    if predecessor[current] is None:
        return False  # No path

    while current != start:
        current.make_path()
        current = predecessor[current]
        draw()

    start.make_start()
    end.make_end()
    return True





def main(win, width):
    rows = 25
    grid = make_grid(rows, width)
    start, end = None, None
    selected_algorithm = "A*"
    negative_mode = False
    run = True
    while run:
        draw(win, grid, rows, width, selected_algorithm)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[1] <= 40:
                    continue
                row, col = get_clicked_pos(pos, rows, width)
                if 0 <= row < rows and 0 <= col < rows:
                    node = grid[row][col]
                    if negative_mode and selected_algorithm == "Bellman-Ford":
                        node.make_negative()
                    elif not start and node != end:
                        start = node
                        start.make_start()
                    elif not end and node != start:
                        end = node
                        end.make_end()
                    elif node != end and node != start:
                        node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                if pos[1] <= 40:
                    continue
                row, col = get_clicked_pos(pos, rows, width)
                if 0 <= row < rows and 0 <= col < rows:
                    node = grid[row][col]
                    node.reset()
                    if node == start:
                        start = None
                    elif node == end:
                        end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_algorithm = "A*"
                elif event.key == pygame.K_2:
                    selected_algorithm = "Dijkstra's"
                elif event.key == pygame.K_3:
                    selected_algorithm = "BFS"
                if event.key == pygame.K_4:
                    selected_algorithm = "Bellman-Ford"
                elif event.key == pygame.K_n and selected_algorithm == "Bellman-Ford":
                    negative_mode = not negative_mode	
                elif event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    if selected_algorithm == "A*":
                        astar(lambda: draw(win, grid, rows, width, selected_algorithm), grid, start, end)
                    elif selected_algorithm == "Dijkstra's":
                        dijkstra(lambda: draw(win, grid, rows, width, selected_algorithm), grid, start, end)
                    elif selected_algorithm == "BFS":
                        bfs(lambda: draw(win, grid, rows, width, selected_algorithm), grid, start, end)
                    elif selected_algorithm == "Bellman-Ford":
                        bellman_ford(lambda: draw(win, grid, rows, width, selected_algorithm), grid, start, end)


                if event.key == pygame.K_c:
                    start, end = None, None
                    grid = make_grid(rows, width)

    pygame.quit()


if __name__ == "__main__":
    main(WIN, WIDTH)

