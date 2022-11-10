from trial import Trial
from level import showLevelWithAgentPNG

def main():
    trial = Trial(map_size = 10, num_agents = 3)
    trial.start_agent_walk(False, False)


    showLevelWithAgentPNG(trial.grid.maze.grid, trial.agents[0].path)
    print(trial.to_json())


if __name__ == '__main__':
    main()