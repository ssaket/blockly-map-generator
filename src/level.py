from dataclasses import dataclass, field
from typing import List, Union

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from dataclasses_json import config, dataclass_json
from mazelib import Maze
from mazelib.generate.AldousBroder import AldousBroder
from mazelib.solve.ShortestPaths import ShortestPaths

from blocks import CodeBlock


@dataclass_json
@dataclass
class Point:
    row: int
    col: int

    def __add__(self, other):
        return Point(self.row + other.row, self.col + other.col)

    def __sub__(self, other):
        return Point(other.row - self.row, other.col - self.col)


@dataclass_json
@dataclass
class Tile(Point):
    value: int = 0
    size: int = 0
    direction: str = field(init=False, default='None')
    code_block: CodeBlock = CodeBlock.EMPTY.value


@dataclass_json
@dataclass
class LevelMap:
    size: int
    map: List[Tile] = field(default_factory=list, repr=False,
                            metadata=config(exclude=lambda x: False))
    maze: Maze = field(init=False, repr=False,
                       metadata=config(exclude=lambda x: True))
    start_location: Union[Point, None] = field(repr=False, default=None)
    score: int = field(default=0)

    def generate_map(self, custom_map=None, algorithm=AldousBroder, seed=121):
        self.maze = Maze(seed)
        if custom_map is not None:
            self.maze.grid = custom_map
        else:
            self.maze.generator = algorithm(self.size, self.size)
            self.maze.generate()
        grid = self.maze.grid
        H, W = grid.shape

        self.map = [Tile(c, r, int(grid[r, c]))
                    for r in range(H) for c in range(W)]

        return self.map

    def find_tile(self, point: Point):
        for i in range(len(self.tiles)):
            if self.tiles[i].x == point.x and self.tiles[i].y == point.y:
                return (self.tiles[i], i)
        return 0

    def _isValid(self, size, level_map, x, y, res):
        if x >= 0 and y >= 0 and x < size and y < size and level_map[x][y].value == 0 and res[x][y].value == 0:
            return True
        return False

    def auto_solver(self, start_location: Tile, end_location: Tile, solver=ShortestPaths()):
        self.maze.start = (start_location.row, start_location.col)
        self.maze.end = (end_location.row, end_location.col)
        self.maze.solver = solver

        try:
            self.maze.solve()
        except:
            print("can't solve the maze")
            showPNGMark(self.maze.grid, self.maze.start, self.maze.end)
        return self.maze.solutions


def print_maze(size, res):
    for i in range(size):
        for j in range(size):
            print(res[i][j], end=' ')
        print()
    print('####################')


def print_level(size, res):
    for i in range(size):
        for j in range(size):
            print(res[i][j].value, end=' ')
        print()
    print('####################')


def showPNG(grid):
    """Generate a simple image of the maze."""
    plt.figure(figsize=(10, 5))
    plt.imshow(grid, cmap=plt.cm.binary, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.show()


def showPNGMark(grid, start, end):
    """Generate a simple image of the maze."""
    plt.figure(figsize=(10, 5))
    plt.imshow(grid, cmap=plt.cm.binary, interpolation='nearest')
    ax = plt.gca()
    start_patch = patches.Circle(start, 0.5, linewidth=3,
                                 edgecolor='r', facecolor='red')
    end_patch = patches.Circle(end, 0.5, linewidth=3,
                               edgecolor='g', facecolor='green')
    ax.add_patch(start_patch)
    ax.add_patch(end_patch)
    plt.xticks([]), plt.yticks([])
    plt.show()


def main():
    size = 4
    level = LevelMap(size)
    map = level.generate_map()
    print(map.tostring(True))
    showPNG(map.grid)


if __name__ == '__main__':
    main()
