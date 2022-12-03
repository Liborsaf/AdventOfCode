# noinspection PyPackageRequirements
from aoc import AdventOfCodeTask


class ThirdDayTask(AdventOfCodeTask):
    def __init__(self):
        self.lower_beginning = ord('a') - 1
        self.upper_beginning = ord('A') - 1
        self.lower_difference = ord('z') - self.lower_beginning
        # self.upper_difference = ord('Z') - self.upper_beginning

    def run(self):
        total_duplicity_items_priority = 0

        for rucksack in self.task_input.split("\n"):
            # Skip last empty line
            if not rucksack:
                continue

            full_size = len(rucksack)
            half_size = full_size // 2

            first_compartment = rucksack[0:half_size]
            second_compartment = rucksack[half_size:full_size]

            duplicity_items = ""

            for item in first_compartment:
                if second_compartment.count(item) > 0 and duplicity_items.count(item) == 0:
                    duplicity_items += item

            duplicity_items_priority = 0

            for item in duplicity_items:
                item_unicode = ord(item)
                item_priority = 0

                if item.islower():
                    item_priority = item_unicode - self.lower_beginning
                elif item.isupper():
                    item_priority = item_unicode - self.upper_beginning + self.lower_difference

                duplicity_items_priority += item_priority

            total_duplicity_items_priority += duplicity_items_priority

            # print(f"Rucksack: {rucksack}, first compartment: {first_compartment}, second compartment: {second_compartment}")

        print(f"Total duplicity items priority: {total_duplicity_items_priority}")
