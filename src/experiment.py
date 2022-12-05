from level import showLevelWithAgentPNG
from trial import Trial
import logging


def main():
    filename = 'blockly-map-generator.log'
    logging.basicConfig(filename=filename,
                        level=logging.INFO)

    logging.info(f'Started logging to {filename}')

    trial = Trial(map_size=8, num_agents=4)
    # trial.generate_map(method='eller', xskew = 0.1, yskew= 0.9)
    # trial.generate_map(method='cellular', complexity=0.2, density=0.2)
    trial.generate_map(mutation=True)
    trial.start_agent_walk(random_start=True)
    trial.show_map_with_agents()

    showLevelWithAgentPNG(trial.__grid[0].maze.grid, trial.__agents[0].path)
    print(trial.to_json())


if __name__ == '__main__':
    main()
