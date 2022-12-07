from __future__ import annotations

import copy
from typing import List, Deque, Optional
from collections import deque

# noinspection PyPackageRequirements
from aoc import AdventOfCodeTask


class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def get_size(self) -> int:
        return self.size


class Directory(File):
    def __init__(self, name: str):
        super().__init__(name, 0)

        self.content = []

    def add_file(self, file: File):
        self.content.append(file)

    def create_directory(self, name: str) -> Directory:
        directory = self.get_item(name)

        if directory:
            return directory

        directory = Directory(name)
        self.content.append(directory)

        return directory

    def get_item(self, name: str) -> Optional[File | Directory]:
        for item in self.content:
            if item.name == name:
                return item

        return None

    def get_items(self) -> List[File | Directory]:
        return self.content

    def print(self, hide_empty: bool = False, level: int = 0):
        start = ''.join(' ' for i in range(level))

        for item in self.content:
            item_size = item.get_size()
            item_type = 'dir' if isinstance(item, Directory) else 'file'

            if item_size > 0 or (item_size == 0 and not hide_empty):
                print(f"{start}- {item.name} ({item_type}, size={item_size})")

                if item_type == 'dir':
                    item.print(hide_empty, level + 1)

                    continue

    def get_size(self) -> int:
        size = super().get_size()

        for item in self.content:
            size += item.get_size()

        return size


class FileSystem(Directory):
    def __init__(self):
        super().__init__('/')

    def get_path(self, path: Deque[str]) -> Optional[File | Directory]:
        directory = self

        for item in path:
            # (directory if directory else self)
            item = directory.get_item(item)

            if isinstance(item, Directory):
                directory = item

                continue

            return item

        return directory

    def make_directory(self, path: Deque[str]):
        directory = self

        for item in path:
            directory = directory.create_directory(item)

    def print(self, hide_empty: bool = False):
        print(f"- / (dir, size={self.get_size()})")

        super().print(hide_empty, 1)


class SeventhDayTask(AdventOfCodeTask):
    def run(self):
        data = self.parameters.input[:-1]

        file_system = FileSystem()

        last_command = ""
        output = []

        current_directory = deque([])

        process_list = []

        for line in data.split("\n"):
            if line.startswith('$'):
                line = line.replace("$ ", "").split(" ")
                command = line[0]
                args = line[1:]

                if output:
                    # print(f"Current directory: {directory.name}")

                    process_list.append((last_command, output, copy.deepcopy(current_directory)))

                    output = []

                # print(f"{command} {args if args else ''}")

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

        for (command, output, current_directory) in process_list:
            directory = file_system.get_path(current_directory)
            assert isinstance(directory, Directory), "Requested path is not directory!"

            if command == 'ls':
                for item in output:
                    # print(f"Verify: {item}")

                    if item.startswith('dir'):
                        item = item.replace('dir ', '')

                        target_directory = directory.get_item(item)

                        assert isinstance(target_directory, Directory), "Target path is not directory!"
                    else:
                        item = item.split(" ")

                        directory.add_file(File(item[1], int(item[0])))

        file_system.print(True)

        print("---")

        size = 0

        for item in file_system.get_items():
            item_size = item.get_size()

            if isinstance(item, Directory) and item_size >= 100_000:
                print(f"{item.name} (size={size})")

                size += item_size

        print("---")
        print(f"Size: {size}")
