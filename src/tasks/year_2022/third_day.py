from typing import List, Optional

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
        current_group = []

        total_duplicity_items_priority = 0
        total_group_duplicity_items_priority = 0

        for rucksack in self.task_input.split("\n"):
            # Skip last empty line
            if not rucksack:
                continue

            current_group.append(rucksack)

            if len(current_group) == self.group_size:
                elves_groups.append(current_group)

                current_group = []

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
            group_badge = ""

            for rucksack in group:
                for item in rucksack:
                    if self.contains_all_in_group(group, item, rucksack):
                        group_badge = item

                        break

            group_badge_priority = self.calculate_items_priority(group_badge)
            print(f"Group: {group} - badge: {group_badge}, priority: {group_badge_priority}")

            total_group_duplicity_items_priority += group_badge_priority

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

    def contains_all_in_group(self, group: List[str], item: str, skip_rucksack: Optional[str] = None) -> bool:
        groups_contains = 0

        for other_rucksack in group:
            if other_rucksack == skip_rucksack:
                continue

            if other_rucksack.count(item) > 0:
                groups_contains += 1

        return groups_contains == self.group_size - 1
