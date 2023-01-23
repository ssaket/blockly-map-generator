# Blockly Map Generator

This project is used to generate maps and agent paths for the blocky plugin. For each trial, the maps are generated using [Eller's algorithm](http://www.neocomputer.org/projects/eller.html). The agent then walks on the map from a random start position to a random end position. The start position is inside the map and the end position is on the edge of the map. The rewards are placed on this path based on random assignment from the outputs of common coding tasks.

## Rewards

Currently, the rewards are generated using the following rules:

- Multiples of Integers (like 1, 2, 5)
- Conditionals (if-else statements)
- Random Sequence of letters

See `reward.py` for more information. **The user is expected to write code to get the rewards from the agent path.**

## How to use

1. Install the python dependencies with conda: `conda env create -f environment.yml`
2. Run the python script: `python experiment.py` with suitable arguments. See the help message for more information: `python experiment.py -h`
3. Save the json file in the `jspsych-blockly` plugin folder to use it in the blocky plugin.

## Structure of the json file

Checkout the [trial.json](./trial.json) for an example of the structure of the json file. The json file contains a list of trials. Each trial contains -

- map: The map of the trial
- agent:
  - path: The agent path of the trial
  - rewards: The rewards of the agent path

## Structure of project

The project is structured as follows:

All the code is in the `src` folder. The `experiment.py` file is the main file. It contains the code to generate the json file. The `reward.py` file contains the code to generate the rewards. The `agent.py` file contains the code to generate the agent paths. The `utils.py` file contains the code to generate plots. The `trial.py` contains code to generate the trials.
