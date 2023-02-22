from datetime import datetime
from typing import List
from trial import Trial
import logging
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Experiment:
    """Generate a set of trials for the experiment.
    
    Args:
        trials (int, optional): The number of trials. Defaults to 10.
    Methods:
        generate_trials: Generate a set of trials.
        show_trial_maps: Show the maps for each trial.
        to_json: Convert the experiment to json.
        save_to_file: Save the experiment to a file.
    """
    trials: int = 10
    trial_list: List[Trial] = field(default_factory=list)

    def __init__(self, trials=10) -> None:
        """Initialize the experiment."""
        self.trials = trials
        self.trial_list = []

    def generate_trials(self):
        """Generate a set of trials for the experiment."""
        for i in range(1, self.trials + 1):
            trial = Trial(i)
            self.trial_list.append(trial)

    def show_trial_maps(self):
        """Show the maps for each trial."""
        for trial in self.trial_list:
            trial.show_map()

    def to_json(self):
        """Convert the experiment to json."""
        return self.to_json()

    def save_to_file(
        self,
        filename=f'blockly-map-generator-{datetime.now().strftime("%Y-%m-%d")}.json'
    ):
        """Save the experiment to a file."""
        data = self.to_json()
        with open(filename, 'w') as f:
            f.write(data)


def main():
    filename = 'blockly-map-generator.log'
    logging.basicConfig(filename=filename, level=logging.INFO)

    logging.info(f'Started logging to {filename}')

    experiment = Experiment(25)
    experiment.generate_trials()

    data = experiment.to_json()
    logging.info(f'Saving data to file')

    filename = f'blockly-map-generator-{datetime.now().strftime("%Y-%m-%d")}.json'
    print(filename)
    experiment.save_to_file(filename)


if __name__ == '__main__':
    main()
