from dataclasses import dataclass, field
from typing import List, Union

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from dataclasses_json import config, dataclass_json
from mazelib import Maze

from mazelib.generate.CellularAutomaton import CellularAutomaton
from mazelib.generate.Ellers import Ellers

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
    grid: List[Tile] = field(default_factory=list, repr=False,
                             metadata=config(exclude=lambda x: False))
    maze: Maze = field(init=False, repr=False,
                       metadata=config(exclude=lambda x: True))

    def generate_map(self, method='cellular', custom_map=None, seed=121, **kwargs):

        self.maze = Maze()
        assert method in [
            'cellular', 'eller'], 'Only Cellular and Eller methods are supported'

        if custom_map is not None:
            self.maze.grid = custom_map
        else:
            if method == 'cellular':
                self.maze.generator = CellularAutomaton(
                    self.size, self.size, **kwargs)
            else:
                self.maze.generator = Ellers(
                    self.size, self.size, **kwargs)
            self.maze.generate()
        grid = self.maze.grid
        H, W = grid.shape

        self.grid = [Tile(c, r, int(grid[r, c]))
                     for r in range(H) for c in range(W)]

        return self.grid



def showLevelPNG(grid):
    """Generate a simple image of the maze."""
    plt.figure(figsize=(10, 5))
    plt.imshow(grid, cmap=plt.cm.binary, interpolation='nearest')
    # plt.xticks([]), plt.yticks([])
    plt.show()


def showLevelWithAgentPNG(grid, agent_paths):
    """Generate a simple image of the maze."""

    nrows = 1
    ncols = len(agent_paths)

    if ncols > 1:
        fig, axes = plt.subplots(
            nrows, ncols, sharex=False, sharey=False)
        for ax in axes.flatten():
            ax.imshow(grid, cmap=plt.cm.binary, interpolation='nearest')
            colors = ['maroon', 'royalblue', 'darkgray', 'coral', 'steelblue']

            for idx, path in enumerate(agent_paths):
                entrance_colors = ['dimgray', 'darkgray']
                for i, tile in enumerate(path):
                    if i == 0 or i == len(path) - 1:
                        color = entrance_colors.pop()
                    else:
                        color = colors[idx]
                    patch = patches.Circle((tile.col, tile.row), 0.5, linewidth=3,
                                           edgecolor=color, facecolor=color)
                    ax.add_patch(patch)
            plt.show()
    else:
        fig, ax = plt.subplots(nrows, ncols, sharex=False,
                               sharey=False, squeeze=True)
        ax.imshow(grid, cmap=plt.cm.binary, interpolation='nearest')
        colors = ['maroon', 'royalblue', 'darkgray', 'coral', 'steelblue']

        for idx, path in enumerate(agent_paths):
            entrance_colors = ['dimgray', 'darkgray']
            for i, tile in enumerate(path):
                if i == 1 or i == len(path) - 1:
                    color = entrance_colors.pop()
                else:
                    color = colors[idx]
                patch = patches.Circle((tile.col, tile.row), 0.5, linewidth=3,
                                       edgecolor=color, facecolor=color)
                ax.add_patch(patch)


def showLevelPNGMark(grid, start, end):
    """Generate a simple image of the maze with start and end marker."""
    plt.figure(figsize=(10, 5))
    plt.imshow(grid, cmap=plt.cm.binary, interpolation='nearest')
    ax = plt.gca()
    start_patch = patches.Circle((start[1], start[0]), 0.5, linewidth=3,
                                 edgecolor='r', facecolor='red')
    end_patch = patches.Circle((end[1], end[0]), 0.5, linewidth=3,
                               edgecolor='g', facecolor='green')
    ax.add_patch(start_patch)
    ax.add_patch(end_patch)
    # plt.xticks([]), plt.yticks([])
    plt.show()