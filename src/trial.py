from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from mazelib import Maze
from mazelib.generate.Ellers import Ellers

from agent import Agent


@dataclass_json
@dataclass
class Trial:
    """Generate a trial for the experiment. A trial is a maze with a set of agents
    that walk through the maze.

    Args:
        id (int, optional): The trial id. Defaults to 1.
    """

    trial_id: int
    maze: Maze = field(init=False, repr=False)  # type: ignore
    agent: Agent = field(init=False, repr=False)

    def __init__(self, id=1) -> None:
        m = Maze()
        size = 3 if id < 3 else 5 if id < 10 else 7
        m.generator = Ellers(size, size)
        m.generate()

        self.maze = m.grid.tolist()
        self.trial_id = id

        self.agent = Agent(self.trial_id, self.maze)

        path_length = self.trial_id if self.trial_id < 5 else None
        self.agent.start_walk(length=path_length)


if __name__ == "__main__":
    t = Trial(1)
    print(t.to_json())
