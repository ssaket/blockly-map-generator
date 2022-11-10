from trial import Trial
from level import showLevelWithAgentPNG

def main():
    trial = Trial(map_size = 8, num_agents = 4)
    # trial.generate_map(method='eller', xskew = 0.1, yskew= 0.9)
    trial.generate_map(method='cellular', complexity=0.2, density=0.2)
    trial.start_agent_walk(random_start=False, random_end=False)
    trial.show_map_with_agents()


    showLevelWithAgentPNG(trial.grid.maze.grid, trial.agents[0].path)
    print(trial.to_json())


if __name__ == '__main__':
    main()