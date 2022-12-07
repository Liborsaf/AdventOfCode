import copy
from typing import List, Deque
from collections import deque

# noinspection PyPackageRequirements
from aoc import AdventOfCodeTask


class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size


class Directory(File):
    def __init__(self, name: str):
        super().__init__(name, 0)

        self.content = {}


class FileSystem(Directory):
    def __init__(self):
        super().__init__('/')

    def get_folder(self, path: Deque[str] | str) -> Directory:
        pass

    def make_directory(self, path: Deque[str]):
        if path:
            first_directory = self.get_folder(path.popleft())
        else:
            first_directory = self

        print(first_directory)

    def print(self):
        pass


class SeventhDayTask(AdventOfCodeTask):
    def run(self):
        data = self.parameters.input[:-1]

        file_system = FileSystem()

        last_command = ""
        output = []

        current_directory = deque([])

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
                        current_directory = deque([])
                    elif args[0] == '..':
                        current_directory.pop()
                    else:
                        current_directory.append(args[0])

                    # print(f"Current directory: {current_directory}")

                    file_system.make_directory(copy.deepcopy(current_directory))

                last_command = command
            else:
                output.append(line)

        print(file_system.print())
