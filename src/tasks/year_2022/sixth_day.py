from typing import List

# noinspection PyPackageRequirements
from aoc import AdventOfCodeTask


class SixthDayTask(AdventOfCodeTask):
    def run(self):
        data = self.parameters.input.replace("\n", "")
        print(f"Data: {data}")

        packet_marker = self.find_marker(data, 4)
        message_marker = self.find_marker(data[packet_marker:], 14) + packet_marker

        print(f"Packer marker: {packet_marker}, message marker: {message_marker}")

    @staticmethod
    def find_marker(data: str | List[str], length: int) -> int:
        marker = 0

        for i in range(len(data) - length + 1):
            sub_data = data[i:i + length]

            if sum([1 for item in sub_data if sub_data.count(item) > 1]) == 0:
                marker = i + length

                break

        return marker
