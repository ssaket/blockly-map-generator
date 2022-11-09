from trial import Trial

def main():
    trial = Trial(1, 5, 4)
    trial.generate_trials(num=10)
    print(trial.to_json())


if __name__ == '__main__':
    main()