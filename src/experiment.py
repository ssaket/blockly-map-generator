from datetime import datetime
from trial import Trial
import logging
import json


class Experiment:
    """Generate a set of trials for the experiment.
    
    Args:
        trials (int, optional): The number of trials. Defaults to 10.
    Methods:
        generate_trials: Generate a set of trials.
        to_json: Convert the experiment to json.

    """

    def __init__(self, trials=10):
        self.trials = trials
        self.trial_list = []

    def generate_trials(self):
        for i in range(1, self.trials + 1):
            trial = Trial(i)
            self.trial_list.append(trial)

    def to_json(self):
        return json.dumps([trial.to_json() for trial in self.trial_list])


def main():
    filename = 'blockly-map-generator.log'
    logging.basicConfig(filename=filename, level=logging.INFO)

    logging.info(f'Started logging to {filename}')

    experiment = Experiment(20)
    experiment.generate_trials()

    data = experiment.to_json()
    logging.info(data)

    filename = f'blockly-map-generator-{datetime.now().strftime("%Y-%m-%d")}.json'
    print(filename)

    # write data to file
    with open(filename, 'w') as f:
        f.write(data)
    print(data)


if __name__ == '__main__':
    main()
