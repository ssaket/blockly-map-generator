# Blockly Map Generator

This is a simple map generator for the [Blockly](https://developers.google.com/blockly/) programming language. The maps can be used in the jsPsych blocky plugin to create a simple programming task. The maps are saved as a JSON file that can be loaded into the blocky plugin.

## How to use

1. Install the python dependencies with conda: `conda env create -f environment.yml`
2. Run the python script: `python experiment.py` with suitable arguments. See the help message for more information: `python experiment.py -h`
3. Save the json file in the `jspsych-blockly` plugin folder to use it in the blocky plugin.

## Structure of the json file

Checkout the [trial.json](./trial.json) for an example of the structure of the json file. The json file contains a list of trials. Each trial contains a list of blocks. Each block contains a list of map and agent path coordinates. The map coordinates are used to draw the map. The agent path coordinates are used to draw the agent path.

## Structure of project

The project is structured as follows:

All the scripts are in the `src` folder. The `experiment.py` script is the main script that generates the json file. The `level.py`, `agent.py`, `blocks.py`, `directions.py` and `trial.py` scripts are used by the `experiment.py` script to generate the json file. More information about the scripts can be found in the comments of the scripts.

In brief, the short description of scripts are as follows:

- `experiment.py`: The main python script that generates the json file.
- `level.py`: The level generator that generates the map and agent path coordinates.
- `agent.py`: The agent that generates the agent path coordinates.
- `blocks.py`: The block generator that generates blockly blocks.
- `directions.py`: The direction generator that generates the directions for the agent.
- `trial.py`: The trial generator that generates the trials for the experiment.
