from aoc import AdventOfCodeTask


class FirstDayTask(AdventOfCodeTask):
    def run(self):
        elves = []
        elf_calories = 0

        for data in self.input.split("\n"):
            if data == '':
                elves.append(elf_calories)
                elf_calories = 0

                continue

            elf_calories += int(data)

        sorted_elves = sorted(elves, reverse=True);

        most_elf = sorted_elves[0]
        most_three_elves = sum(sorted_elves[:3])

        print(f"Most elf total: {most_elf}, Most 3 elves total: {most_three_elves}")

class SecondDayTask(AdventOfCodeTask):
    opponent_mapping = {
        'A': 'Rock',
        'B': 'Paper',
        'C': 'Scissors'
    }

    def run(self):
        print(self.input)
