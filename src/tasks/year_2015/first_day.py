# noinspection PyPackageRequirements
from aoc import AdventOfCodeTask


# https://adventofcode.com/2015/day/1
class FirstDayTask(AdventOfCodeTask):
    def run(self):
        floor = 0
        basement_character_index = 0

        for i in range(len(self.parameters.input)):
            character = self.parameters.input[i]

            if character == '(':
                floor += 1
            elif character == ')':
                floor -= 1

            if basement_character_index == 0 and floor == -1:
                basement_character_index = i + 1  # Add 1, because counting of characters starts from 1 not 0

        print(f"Floor: {floor}, basement character index: {basement_character_index}")
