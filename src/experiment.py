from trial import Trial
from utils import showLevelWithAgentPNG
import logging


def main():
    filename = 'blockly-map-generator.log'
    logging.basicConfig(filename=filename, level=logging.INFO)

    logging.info(f'Started logging to {filename}')

    trial = Trial(id=21)
    showLevelWithAgentPNG(trial.maze, trial.agent.path)
    # trial.generate_map(method='eller', xskew = 0.1, yskew= 0.9)
    # trial.generate_map(method='cellular', complexity=0.2, density=0.2)
    # trial.generate_map(mutation=True)
    # trial.start_agent_walk(random_start=True)
    # trial.show_map_with_agents()
    print(trial.to_json())


if __name__ == '__main__':
    main()
