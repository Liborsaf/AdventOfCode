# noinspection PyPackageRequirements
from aoc import AdventOfCodeTask


class SeventhDayTask(AdventOfCodeTask):
    def run(self):
        data = self.parameters.input[:-1]

        last_command = ""
        output = []

        current_directory = ""

        for line in data.split("\n"):
            if line.startswith('$'):
                line = line.replace("$ ", "").split(" ")
                command = line[0]
                args = line[1:]

                if output:
                    if last_command == 'ls':
                        print(output)

                    output = []

                print(f"{command} {args if args else ''}")

                if command == 'cd':
                    if args[0] == '/':
                        current_directory = '/'
                    elif args[0] == '..':
                        # current_directory = current_directory[1:-1]
                        # current_directory = '/'.join(current_directory.split("/")[:-1])
                        # current_directory = current_directory + '/'

                        current_directory = '/'.join(current_directory.split("/")[:-2]) + '/'
                    else:
                        current_directory += args[0] + '/'

                    print(f"Current directory: {current_directory}")

                last_command = command
            else:
                output.append(line)
