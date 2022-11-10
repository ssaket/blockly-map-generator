from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List


from agent import Agent
from level import LevelMap


@dataclass_json
@dataclass
class Trial:
    """
    Generate a trial for the experiment
    """
    id: int = field(default=1)
    map_size: int = field(default=5)
    num_agents: int = field(default=3)
    grid: LevelMap = field(init=False, repr=False)
    agents: List[Agent] = field(default_factory=list, repr=False)

    def __post_init__(self):
        level = LevelMap(self.map_size)
        level.generate_map(complexity = 0.1, density = 0.2)
        self.grid = level
        for id in range(1, self.num_agents + 1):
            self.agents.append(Agent(id, self.grid))

    def start_agent_walk(self, random_start = False, random_end = True):
        for agent in self.agents:
            agent.start_walk(random_start, random_end)


    def generate_custom_trial(self, custom_map):
        """
        Generate trial based on given numpy maze array
        """
        level = LevelMap(custom_map.shape[0] // 2 - 1)
        level.generate_map(custom_map)

        for id in range(1, self.num_agents + 1):
            self.agents.append(Agent(id, level))
        for agent in self.agents:
            agent.start_walk()

        self.grid = level


def main():
    trial = Trial(1, 5, 4)
    # showPNG(trial.trial_map.maze.grid)
    trial.generate_trials(num=10)
    print(trial.to_json())


if __name__ == '__main__':
    main()
