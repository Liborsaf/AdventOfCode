# noinspection PyPackageRequirements
from aoc import AdventOfCodeTask


# https://adventofcode.com/2015/day/1
class FourthDayTask(AdventOfCodeTask):
    def run(self):
        fully_contains_pairs = 0

        for pair in self.task_input.split("\n"):
            if not pair:
                continue

            (first_pair, second_pair) = pair.split(",")

            (first_pair_min, first_pair_max) = first_pair.split("-")
            (second_pair_min, second_pair_max) = second_pair.split("-")

            first_pair_min = int(first_pair_min)
            first_pair_max = int(first_pair_max)

            second_pair_min = int(second_pair_min)
            second_pair_max = int(second_pair_max)

            fully_contains = True

            """
            for i in range(first_pair_min, first_pair_max):
                result = self.is_in_range(i, second_pair_min, second_pair_max)
                print(f"Check 1: {result}")

                if not result:
                    fully_contains = False

                    break
            """
            first_pair_numbers = [i for i in range(first_pair_min, first_pair_max + 1)]

            for i in range(second_pair_min, second_pair_max + 1):
                if first_pair_numbers.count(i) == 0:
                    fully_contains = False

            if not fully_contains:
                fully_contains = True

                """
                for i in range(second_pair_min, second_pair_max):
                    result = self.is_in_range(i, first_pair_min, first_pair_max)
                    print(f"Check 2: {result}")

                    if not result:
                        fully_contains = False

                        break
                """

                second_pair_numbers = [i for i in range(second_pair_min, second_pair_max + 1)]

                for i in range(first_pair_min, first_pair_max + 1):
                    if second_pair_numbers.count(i) == 0:
                        fully_contains = False

            if fully_contains:
                fully_contains_pairs += 1
            else:
                print(f"First: {first_pair}, second: {second_pair}, contains: {fully_contains}")

        print(f"{fully_contains_pairs}")

    @staticmethod
    def is_in_range(x: int, min: int, max: int) -> bool:
        print(f"Test {min} < {x} < {max}")

        return min <= x <= max
