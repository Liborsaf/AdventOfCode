import tomllib

# noinspection PyPackageRequirements
from aoc import AdventOfCode

from tasks import *


# noinspection PyUnresolvedReferences
def main():
    config = load_config()

    instance = AdventOfCode(2022)
    instance.enable_auto_input_fetch(config['remote']['session'], True)
    # instance.set_input("Hello, world!")

    # instance.enable_debug()

    instance.register_task(1, FirstDayTask2022)
    instance.register_task(2, SecondDayTask2022)
    instance.register_task(3, ThirdDayTask2022)
    instance.register_task(4, FourthDayTask2022)
    instance.register_task(5, FifthDayTask2022)
    instance.register_task(6, SixthDayTask2022)
    instance.register_task(7, SeventhDayTask2022)

    instance.add_year(2016)

    instance.register_task(1, FirstDayTask2016)

    instance.add_year(2015)

    instance.register_task(1, FirstDayTask2015)
    instance.register_task(2, SecondDayTask2015)
    instance.register_task(3, ThirdDayTask2015)

    # instance.execute_all()
    # instance.execute_all(year=2022)
    # instance.execute_last()
    # instance.execute_last(year=2016)
    instance.execute_last(year=2022)
    # instance.execute(2, year=2022)
    # instance.execute(4, year=2022, variant=1)


def load_config() -> object:
    with open("config.toml", "rb") as file:
        config = tomllib.load(file)

    return config


if __name__ == '__main__':
    main()
