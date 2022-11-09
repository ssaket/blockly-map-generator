from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List


from agent import Agent
from level import LevelMap


@dataclass_json
@dataclass
class Trial:
    """
    Generate trials for the experiment
    """
    trial_num: int
    map_size: int = field(default=5)
    num_agent: int = field(default=3)
    trial_map: LevelMap = field(init=False, repr=False)
    agents: List[Agent] = field(default_factory=list, repr=False)

    def generate_trials(self, num: int):
        """
        Generate trials
        """
        level = LevelMap(self.map_size)
        level.generate_map()

        for trial in range(num):
            for id in range(1, self.num_agent + 1):
                self.agents.append(Agent(id, level))
            self.trial_map = level
            for agent in self.agents:
                agent.start_walk()

    def generate_custom_trial(self, custom_map):
        """
        Generate trial based on given numpy maze array
        """
        level = LevelMap(self.map_size)
        level.generate_map(custom_map)

        for id in range(1, self.num_agent + 1):
            self.agents.append(Agent(id, level))
        self.trial_map = level
        for agent in self.agents:
            agent.start_walk()


def main():
    trial = Trial(1, 5, 4)
    # showPNG(trial.trial_map.maze.grid)
    trial.generate_trials(num=10)
    print(trial.to_json())


if __name__ == '__main__':
    main()
