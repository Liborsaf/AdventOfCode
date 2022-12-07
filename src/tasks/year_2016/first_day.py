# noinspection PyPackageRequirements
from aoc import AdventOfCodeTask
from enum import Enum


class Direction(Enum):
    North = 0
    West = 1
    South = 2
    East = 3


class FirstDayTask(AdventOfCodeTask):
    def __init__(self):
        self.direction_mapping = {}

        self.calculate_direction_mapping()

        print(self.direction_mapping)

    def run(self):
        data = self.parameters.input.replace("\n", "").split(", ")

        direction = Direction.North

        for step in data:
            direction = step[0]
            blocks = int(step[1:])

            print(f"{direction} {blocks}")

    def calculate_direction_mapping(self):
        for arg in 'LR':
            for direction in Direction:
                self.direction_mapping[(arg, direction)] = self.get_direction(direction, arg)

    @staticmethod
    def get_direction(current_direction: Direction, arg: str):
        index = current_direction.value

        if arg == 'L':
            index -= 1
        elif arg == 'R':
            index += 1

        directions = len(Direction)

        if index < 0:
            diff = directions - index
            index = diff - 1

        elif index > len(Direction):
            diff = abs(len(Direction) - index)
            index = diff

        print(index)

        return Direction(index - 1)
