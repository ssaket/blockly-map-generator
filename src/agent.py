from dataclasses import dataclass, field
from typing import List

from dataclasses_json import config, dataclass_json
from mazelib.solve.Chain import Chain

from blocks import CodeBlock
from direction import DirectionEnum
from level import LevelMap, Tile, showLevelPNGMark
import logging

# define possible ways to turn left for the agent
TURN_LEFT = [
    [DirectionEnum.SOUTH, DirectionEnum.EAST],
    [DirectionEnum.NORTH, DirectionEnum.WEST],
    [DirectionEnum.EAST, DirectionEnum.NORTH],
    [DirectionEnum.WEST, DirectionEnum.SOUTH],
]
# define possible ways to turn right for the agent
TURN_RIGHT = [
    [DirectionEnum.SOUTH, DirectionEnum.WEST],
    [DirectionEnum.NORTH, DirectionEnum.EAST],
    [DirectionEnum.EAST, DirectionEnum.SOUTH],
    [DirectionEnum.WEST, DirectionEnum.NORTH],
]
# define possible ways to turn around (180 degrees) for the agent
TURN_AROUND = [
    [DirectionEnum.SOUTH, DirectionEnum.NORTH],
    [DirectionEnum.EAST, DirectionEnum.WEST],
    [DirectionEnum.NORTH, DirectionEnum.SOUTH],
    [DirectionEnum.WEST, DirectionEnum.EAST],
]


@dataclass_json
@dataclass
class Agent:
    """A computer agent who can walk on the map using different strategy to solve the maze."""
    id: int
    grid: LevelMap
    curr_direction: DirectionEnum
    path: List[List[Tile]] = field(
        default_factory=list,
        metadata=config(exclude=lambda x: False))  # type: ignore

    def auto_solver(self, start_location, end_location,
                    solver=Chain()) -> list[list]:
        """Automatically solve the maze using the given solver."""

        self.grid.maze.start = (start_location.row, start_location.col)
        self.grid.maze.end = (end_location.row, end_location.col)
        self.grid.maze.solver = solver  # type: ignore

        try:
            logging.info('start solving maze...')
            self.grid.maze.solve()
            logging.info('maze is solved!')
        except:
            print("can't solve the maze")
            showLevelPNGMark(self.grid.maze.grid, self.grid.maze.start,
                             self.grid.maze.end)
        return self.grid.maze.solutions  # type: ignore

    def start_walk(self, start_tile, end_tile):
        """Start walking on the map."""

        paths = self.auto_solver(start_tile, end_tile)

        for path in paths:
            old_tile = start_tile
            old_direction = self.curr_direction
            path.append((end_tile.row, end_tile.col))

            tiles: List[Tile] = []
            for location in path:
                x, y = location
                new_tile = Tile(int(x), int(y))
                delta = old_tile - new_tile
                new_direction = DirectionEnum((delta.row, delta.col))
                self.curr_direction = new_direction

                if old_direction == new_direction:
                    new_tile.code_block = CodeBlock.MOVE_FORWARD.value
                elif [old_direction, new_direction] in TURN_AROUND:
                    new_tile.code_block = '#'.join([
                        CodeBlock.TURN_LEFT.value, CodeBlock.TURN_LEFT.value,
                        CodeBlock.MOVE_FORWARD.value
                    ])
                elif [old_direction, new_direction] in TURN_LEFT:
                    new_tile.code_block = '#'.join([
                        CodeBlock.TURN_LEFT.value, CodeBlock.MOVE_FORWARD.value
                    ])
                elif [old_direction, new_direction] in TURN_RIGHT:
                    new_tile.code_block = '#'.join([
                        CodeBlock.TURN_RIGHT.value, CodeBlock.MOVE_FORWARD.value
                    ])

                old_tile = new_tile
                old_direction = new_direction
                tiles.append(new_tile)
            self.path.append(tiles)

            logging.info('done walking!')
            return tiles
