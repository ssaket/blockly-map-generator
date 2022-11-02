
# seed the pseudorandom number generator
from random import choice, choices, randint, seed


import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from level import LevelMap, Tile
from agent import Agent

# seed random number generator
seed(1)

# actions
ACTION = ['move_forward', 'turn_left', 'turn_right', 'turn_left$move_forward',
          'turn_right$move_forward', 'move_forward$move_forward']

# programming operators
OPERATORS = ['if', 'if_else', 'while', 'do_while']

# number of agents
TOTAL_AGENTS = 3

# direction
DIRECTION = ['north', 'south', 'east', 'west']

# size
size = [20, 20]


def main():
    level = LevelMap()
    level_map = level.generate_empty_map(20, Tile(20 // 2, 20 //2))

    for agent_id in range(1, TOTAL_AGENTS + 1):
        agent = Agent(agent_id, level_map)
        total_steps = randint(1, 5)

        while (total_steps >= 0):
            basket_size = randint(1, 10)
            actions = choices(
                ACTION, weights=[0.2, 0.1, 0.1, 0.2, 0.2, 0.2], k=basket_size)
            for action in actions:
                for sub_action in action.split('$'):
                    agent.perform_action(sub_action)
                total_steps -= 1
        print(agent.path)
        dfS = pd.DataFrame(mesh_coords)

    df = pd.DataFrame(mesh_coords)
    print(df.head())
    print(df.shape)
    sns.scatterplot(data=df, x='x', y='y', hue='visited_agent')
    plt.show()

    # while (total_steps > 0):


if __name__ == '__main__':
    main()
