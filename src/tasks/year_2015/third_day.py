from typing import Optional

# noinspection PyPackageRequirements
from aoc import AdventOfCodeTask


class House:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


# https://adventofcode.com/2015/day/3
class ThirdDayTask(AdventOfCodeTask):
    def __init__(self):
        self.houses = []

    def run(self):
        x = 0
        y = 0

        moves = len(self.parameters.input)
        more_presents_houses = 0

        for direction in self.parameters.input:
            if direction == '^':
                y += 1
            elif direction == '<':
                x -= 1
            elif direction == 'v':
                y -= 1
            elif direction == '>':
                x += 1

            if self.get_house(x, y):
                more_presents_houses += 1
            else:
                self.houses.append(House(x, y))

        print(f"X: {x}, Y: {y}, total moves: {moves}, houses with more presents: {more_presents_houses}")

    def get_house(self, x: int, y: int) -> Optional[House]:
        for house in self.houses:
            if house.x == x and house.y == y:
                return house

        return None
