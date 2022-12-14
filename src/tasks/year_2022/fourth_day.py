# noinspection PyPackageRequirements
from aoc import AdventOfCodeTask, AdventOfCodeTaskVariant


class FourthDayTask(AdventOfCodeTask):
    def __init__(self):
        self.add_variant(1, FourthDayTaskFirstVariant)
        self.add_variant(2, FourthDayTaskSecondVariant)


# https://adventofcode.com/2015/day/1
class FourthDayTaskFirstVariant(AdventOfCodeTaskVariant):
    def run(self):
        fully_contains_pairs = 0
        partially_contains_pairs = 0

        for pair in self.parameters.input.split("\n"):
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
            partially_contains = False

            first_pair_numbers = [i for i in range(first_pair_min, first_pair_max + 1)]

            for i in range(second_pair_min, second_pair_max + 1):
                if first_pair_numbers.count(i) == 0:
                    fully_contains = False
                else:
                    partially_contains = True

            if not fully_contains:
                fully_contains = True

                second_pair_numbers = [i for i in range(second_pair_min, second_pair_max + 1)]

                for i in range(first_pair_min, first_pair_max + 1):
                    if second_pair_numbers.count(i) == 0:
                        fully_contains = False
                    else:
                        partially_contains = True

            if fully_contains:
                fully_contains_pairs += 1
            # else:
            #    print(f"First: {first_pair}, second: {second_pair}, contains: {fully_contains}")

            if partially_contains:
                partially_contains_pairs += 1

        print(f"{fully_contains_pairs}")
        print(f"{partially_contains_pairs}")


class FourthDayTaskSecondVariant(AdventOfCodeTaskVariant):
    def run(self):
        print("Hello, world!")
