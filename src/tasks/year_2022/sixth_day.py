# noinspection PyPackageRequirements
from aoc import AdventOfCodeTask


class SixthDayTask(AdventOfCodeTask):
    def run(self):
        data = self.parameters.input.replace("\n", "")
        print(data)

        packet_marker = 0

        for i in range(len(data) - 3):
            sublist = data[i:i + 4]

            if packet_marker == 0 and sum([1 for item in sublist if sublist.count(item) > 1]) == 0:
                packet_marker = i + 4

        packet = data[packet_marker:]

        message_marker = 0

        for i in range(len(packet) - 13):
            sublist = packet[i:i + 14]

            if message_marker == 0 and sum([1 for item in sublist if sublist.count(item) > 1]) == 0:
                message_marker = i + 14

        print(packet_marker)
        print(packet_marker + message_marker)
