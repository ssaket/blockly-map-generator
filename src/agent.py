from dataclasses import dataclass, field
from typing import List

from dataclasses_json import config, dataclass_json
from mazelib.solve.Chain import Chain
from mazelib import Maze
from rewards import Rewards
import random
import numpy as np


@dataclass_json
@dataclass
class Agent:
    """An agent that walks through a maze.
    Args:
        id (int): The agent id.
        map (List[List[int]]): The maze map.

    Methods:
        start_walk(length, random_start): Start the agent walk.
    """
    agent_id: int
    path: List[List[int]] = field(default_factory=list)
    rewards: List[int] = field(default_factory=list)
    map: List[List[int]] = field(
        default_factory=list,
        repr=False,
        metadata=config(exclude=lambda x: True))  # type: ignore

    def __init__(self, id, map):
        """Initialize the agent."""
        self.agent_id = id
        self.map = map

    def start_walk(self, length, random_start=False):
        """Start the agent walk."""
        m = Maze()
        m.grid = np.array(self.map)

        # m.start = (1, 0)
        # m.end = (5, 5)
        m.generate_entrances(start_outer=True, end_outer=True)
        m.solver = Chain()  # type: ignore
        m.solve()
        if length is not None:
            print( m.solutions)
            self.path = m.solutions[0][:length]  # type: ignore
            # print(f'length: {len(m.solutions[0]}')
        else:
            self.path = m.solutions[0]  # type: ignore

        random_choice = random.choice(list(Rewards))
        self.rewards = random_choice.value[1](len(self.path))
