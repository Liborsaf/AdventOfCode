# noinspection PyPackageRequirements
from aoc import AdventOfCodeTask


class ThirdDayTask(AdventOfCodeTask):
    group_size = 3

    def __init__(self):
        self.lower_beginning = ord('a') - 1
        self.upper_beginning = ord('A') - 1
        self.lower_difference = ord('z') - self.lower_beginning
        # self.upper_difference = ord('Z') - self.upper_beginning

    def run(self):
        elves_groups = []
        current_elf = []

        total_duplicity_items_priority = 0
        total_group_duplicity_items_priority = 0

        for rucksack in self.task_input.split("\n"):
            # Skip last empty line
            if not rucksack:
                continue

            if len(current_elf) == self.group_size:
                elves_groups.append(current_elf)

                current_elf = []

            current_elf.append(rucksack)

            half_size = len(rucksack) // 2

            first_compartment = rucksack[:half_size]
            second_compartment = rucksack[half_size:]

            duplicity_items = ""

            for item in first_compartment:
                if second_compartment.count(item) > 0 and duplicity_items.count(item) == 0:
                    duplicity_items += item

            total_duplicity_items_priority += self.calculate_items_priority(duplicity_items)

            # print(f"Rucksack: {rucksack}, first compartment: {first_compartment}, second compartment: {second_compartment}")

        for group in elves_groups:
            rucksack = ''.join(group)

            duplicity_items = ""

            for item in rucksack:
                if rucksack.count(item) == self.group_size and duplicity_items.count(item) == 0:
                    duplicity_items += item

            print(rucksack)

            total_group_duplicity_items_priority += self.calculate_items_priority(duplicity_items)

        print(f"Total duplicity items priority: {total_duplicity_items_priority}, total duplicity items priority of {self.group_size} elves group: {total_group_duplicity_items_priority}")

    def calculate_items_priority(self, items: str) -> int:
        total_priority = 0

        for item in items:
            item_unicode = ord(item)
            item_priority = 0

            if item.islower():
                item_priority = item_unicode - self.lower_beginning
            elif item.isupper():
                item_priority = item_unicode - self.upper_beginning + self.lower_difference

            total_priority += item_priority

        return total_priority
