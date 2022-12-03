from typing import List

# noinspection PyPackageRequirements
from aoc import AdventOfCodeTask


class FirstDayTask(AdventOfCodeTask):
    def run(self):
        elves = self.sum_elves()

        sorted_elves = sorted(elves, reverse=True)

        most_elf = sorted_elves[0]
        most_three_elves = sum(sorted_elves[:3])

        print(f"Most elf total: {most_elf}, Most 3 elves total: {most_three_elves}")

    def sum_elves(self) -> List[int]:
        elves = []
        elf_calories = 0

        for data in self.task_input.split("\n"):
            if data == '':
                elves.append(elf_calories)
                elf_calories = 0

                continue

            elf_calories += int(data)

        return elves
