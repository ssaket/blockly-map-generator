#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from random import choices
from typing import List, Union

from mazelib import Maze
from mazelib.generate.AldousBroder import AldousBroder

from blocks import CodeBlock


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


@dataclass
class Tile(Point):
    value: str = 0
    visiting_agent: List = field(default_factory=list)
    code_block: CodeBlock = CodeBlock.EMPTY


@dataclass
class LevelMap:
    size: int
    map: List[Tile] = field(default_factory=list)
    maze: Maze = field(init=False, repr=False)
    start_location: Union[Point, None] = field(repr=False, default=None)
    score: int = field(default=0)

    def generate_map(self, algorithm=AldousBroder):
        self.maze = Maze()
        self.maze.generator = algorithm(self.size, self.size)

        self.maze.generate()
        grid = self.maze.grid
        H, W = grid.shape

        self.map = [Tile(c, r, grid[r, c]) for r in range(H) for c in range(W)]

        return self.maze

    def find_tile(self, point: Point):
        for i in range(len(self.tiles)):
            if self.tiles[i].x == point.x and self.tiles[i].y == point.y:
                return self.tiles[i]
        return 0

    def find_tile_index(self, point: Point):
        for i in range(len(self.tiles)):
            if self.tiles[i].x == point.x and self.tiles[i].y == point.y:
                return i
        return 0

    def isValid(self, size, level_map, x, y, res):
        if x >= 0 and y >= 0 and x < size and y < size and level_map[x][y].value == 0 and res[x][y].value == 0:
            return True
        return False

    def level_maze(self, size, maze, move_x, move_y, x, y, end_x, end_y, res):
        # if (x, y is goal) return True
        if x == end_x and y == end_y:
            return True
        for i in range(4):
            # Generate new value of x
            x_new = x + move_x[i]

            # Generate new value of y
            y_new = y + move_y[i]

            # Check if maze[x][y] is valid
            if self.isValid(size, maze, x_new, y_new, res):

                # mark x, y as part of solution path
                res[x_new][y_new].value = 1
                if self.level_maze(size, maze, move_x, move_y, x_new, y_new, end_x, end_y, res):
                    return True
                res[x_new][y_new].value = 0
        return False

    def solve_maze(self, maze: List[Tile], start_location: Tile, end_location: Tile):
        # Creating a size * size 2-D list
        res = [[Tile(i, j) for j in range(self.size)]
               for i in range(self.size)]
        res[start_location.x][start_location.y].value = 1

        # x matrix for each direction
        move_x = [-1, 1, 0, 0]

        # y matrix for each direction
        move_y = [0, 0, -1, 1]

        if self.level_maze(self.size, maze, move_x, move_y, start_location.x, start_location.y, end_location.x, end_location.y, res):
            print_level(self.size, res)
        else:
            print('Solution does  not exist')
        return res


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


def main():
    size = 4
    level = LevelMap(size)
    map = level.generate_map()
    print(map.tostring(True))
    showPNG(map.grid)


if __name__ == '__main__':
    main()
