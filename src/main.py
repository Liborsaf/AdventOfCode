import tomllib

# noinspection PyPackageRequirements
from aoc import AdventOfCode

# from tasks import FirstDayTask, SecondDayTask
from tasks.first_day import FirstDayTask
from tasks.second_day import SecondDayTask


# noinspection PyUnresolvedReferences
def main():
    config = load_config()

    instance = AdventOfCode(2022)
    instance.enable_auto_input_fetch(config['remote']['session'], True)

    instance.register_task(1, FirstDayTask)
    instance.register_task(2, SecondDayTask)

    instance.execute(2)
    # instance.execute_last()


def load_config() -> object:
    with open("config.toml", "rb") as file:
        config = tomllib.load(file)

    return config


if __name__ == '__main__':
    main()
