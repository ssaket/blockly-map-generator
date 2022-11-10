from enum import Enum
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from typing import List, Union
from direction import DirectionEnum
from level import LevelMap, Tile, Point, showLevelPNGMark
from mazelib.solve.Chain import Chain
from mazelib.solve.ShortestPath import ShortestPath
from random import choice
from blocks import CodeBlock
import numpy as np

# actions
TURN_LEFT = [
    [DirectionEnum.SOUTH, DirectionEnum.EAST],
    [DirectionEnum.NORTH, DirectionEnum.WEST],
    [DirectionEnum.EAST, DirectionEnum.NORTH],
    [DirectionEnum.WEST, DirectionEnum.SOUTH],
]

TURN_RIGHT = [
    [DirectionEnum.SOUTH, DirectionEnum.WEST],
    [DirectionEnum.NORTH, DirectionEnum.EAST],
    [DirectionEnum.EAST, DirectionEnum.SOUTH],
    [DirectionEnum.WEST, DirectionEnum.NORTH],
]

TURN_AROUND = [
    [DirectionEnum.SOUTH, DirectionEnum.NORTH],
    [DirectionEnum.EAST, DirectionEnum.WEST],
    [DirectionEnum.NORTH, DirectionEnum.SOUTH],
    [DirectionEnum.WEST, DirectionEnum.EAST]
]

# direction coords for actions
class ActionEnum(Enum):
    MOVE = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)


@dataclass_json
@dataclass
class Agent:
    id: int
    grid: LevelMap
    current_location: Union[Point, None] = None
    direction: DirectionEnum = choice(list(DirectionEnum))
    path: List[Tile] = field(default_factory=list,
                             metadata=config(exclude=lambda x: False))

    def auto_solver(self, start_location, end_location, solver=Chain()):
        
        self.grid.maze.start = (start_location.row, start_location.col)
        self.grid.maze.end = (end_location.row, end_location.col)
        self.grid.maze.solver = solver

        try:
            print('start solving maze...')
            self.grid.maze.solve()
            print('maze is solved!')
        except:
            print("can't solve the maze")
            showLevelPNGMark(self.grid.maze.grid, self.grid.maze.start, self.grid.maze.end)
        return self.grid.maze.solutions


    def start_walk(self, start_tile, end_tile):

        paths = self.auto_solver(start_tile, end_tile)
        start_tile.direction = self.direction.name

        for path in paths:
            old_tile = start_tile
            old_direction = self.direction
            tiles = [start_tile]
            for location in path:
                x, y = location
                new_tile = Tile(int(x), int(y))
                delta = old_tile - new_tile
                new_direction = DirectionEnum((delta.row, delta.col))
                new_tile.direction = new_direction.name

                if old_direction == new_direction:
                    new_tile.code_block = CodeBlock.MOVE_FORWARD.value
                elif [old_direction, new_direction] in TURN_AROUND:
                    new_tile.code_block = '#'.join(
                        [CodeBlock.TURN_LEFT.value, CodeBlock.TURN_LEFT.value, CodeBlock.MOVE_FORWARD.value])
                elif [old_direction, new_direction] in TURN_LEFT:
                    new_tile.code_block = '#'.join(
                        [CodeBlock.TURN_LEFT.value, CodeBlock.MOVE_FORWARD.value])
                elif [old_direction, new_direction] in TURN_RIGHT:
                    new_tile.code_block = '#'.join(
                        [CodeBlock.TURN_RIGHT.value, CodeBlock.MOVE_FORWARD.value])

                old_tile = new_tile
                old_direction = new_direction
                tiles.append(new_tile)
            tiles.append(end_tile)
            self.path.append(tiles)
        
            print('done walking!')
            return tiles
