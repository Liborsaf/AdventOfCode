import copy
from typing import Dict, List

# noinspection PyPackageRequirements
from aoc import AdventOfCodeTask


# https://adventofcode.com/2022/day/5
class FifthDayTask(AdventOfCodeTask):
    def run(self):
        lines = self.parameters.input.split("\n")

        stacks = {}

        last_stacks_index = 9

        # Parse stacks
        for i in range(last_stacks_index - 1):
            line = lines[i]
            print(line)

            for j in range((len(line) // 3) - 2):
                crate = line[1 + (j * 4)]
                index = j + 1

                if crate == ' ':
                    continue

                if index in stacks:
                    stacks[index].insert(0, crate)
                else:
                    stacks[index] = [crate]

        second_stacks = copy.deepcopy(stacks)

        for instruction in lines[last_stacks_index + 1:]:
            if not instruction:
                continue

            instruction = instruction.replace("move", "").replace(" ", "")
            instruction = instruction.split("from")

            count = int(instruction[0])

            instruction = instruction[1].split("to")

            from_stack_index = int(instruction[0])
            to_stack_index = int(instruction[1])

            from_stack = stacks[from_stack_index]
            to_stack = stacks[to_stack_index]

            print(f"From: {from_stack}, to: {to_stack}, count: {count}")

            # Part 1:
            for i in range(count):
                to_stack.append(from_stack.pop())

            print(f"Result, from: {from_stack}, to: {to_stack}, count: {count}")

            from_second_stack = second_stacks[from_stack_index]
            to_second_stack = second_stacks[to_stack_index]

            print(f"From second: {from_second_stack}, to: {to_second_stack}, count: {count}")

            # Part 2:
            temp_stack = [from_second_stack.pop() for i in range(count)]
            temp_stack.reverse()

            for crate in temp_stack:
                to_second_stack.append(crate)

        # stacks = sorted(stacks)
        print(f"Final stacks: {stacks}")
        print(f"Final second stacks: {second_stacks}")

        result = self.get_result(stacks)
        second_result = self.get_result(second_stacks)

        print(f"Result: {result}, second result: {second_result}")

    @staticmethod
    def get_result(stacks: Dict[int, List[str]]) -> str:
        result = ""

        for stack in sorted(stacks):
            result += stacks[stack][-1]

        return result
