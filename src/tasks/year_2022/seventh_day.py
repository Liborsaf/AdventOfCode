from __future__ import annotations

from typing import List, Optional, TypedDict
from typing_extensions import Unpack

# noinspection PyPackageRequirements
from aoc import AdventOfCodeTask


debug_level = 2


class DirectoryPrintArgs(TypedDict):
    level: int
    hide_empty: bool


class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def get_size(self) -> int:
        return self.size

    def is_directory(self) -> bool:
        return False


class Directory(File):
    def __init__(self, name: str):
        super().__init__(name, 0)

        self.content = []

    def create_directory(self, path: List[str]) -> Directory:
        directory = self

        for item in path:
            directory = directory.__create_directory(item)

        return directory

    def __create_directory(self, name: str) -> Directory:
        item = self.__get_item(name)

        if item:
            assert item.is_directory(), "Requested directory name is already used for file!"

            return item

        item = Directory(name)
        self.content.append(item)

        return item

    def add_file(self, file: File):
        self.content.append(file)

    def print(self, **kwargs: Unpack[DirectoryPrintArgs]):
        kwargs.setdefault('level', 1)
        level = kwargs.get('level')

        kwargs.setdefault('hide_empty', False)
        hide_empty = kwargs.get('hide_empty')

        start = ''.join(' ' for _ in range(level))

        # print(f"{start}- {self.name} (dir, size={self.get_size()})")

        for item in self.content:
            item_size = item.get_size()
            item_type = 'dir' if item.is_directory() else 'file'

            if item_size > 0 or (item_size == 0 and not hide_empty):
                print(f"{start}- {item.name} ({item_type}, size={item_size})")

                if item.is_directory():
                    item.print(level=(level + 1), hide_empty=hide_empty)

    def get_item(self, path: List[str]) -> Optional[File | Directory]:
        directory = self

        for item in path:
            item = directory.__get_item(item)

            if not item:
                return None

            if item.is_directory():
                directory = item

                continue

            return item

        # return None if directory == self else directory
        return directory

    def __get_item(self, name: str) -> Optional[File | Directory]:
        for item in self.content:
            if item.name == name:
                return item

        return None

    def get_items(self):
        return self.content

    def get_size(self) -> int:
        size = super().get_size()

        for item in self.content:
            size += item.get_size()

        return size

    def is_directory(self) -> bool:
        return True


class FileSystem(Directory):
    def __init__(self):
        super().__init__('/')

        self.current_path = []

    def change_directory(self, directory: str):
        # print(f"Going directory to '{directory}'")

        if directory == '/':
            self.current_path = []
        elif directory == '..':
            self.current_path.pop()
        else:
            self.current_path.append(directory)

        self.create_directory(self.current_path)

        # print(f"Directory changed to {self.current_path}")

    def list_directory(self, content: List[str]):
        if debug_level >= 3:
            print(f"Listing directory {self.current_path}")

        for item in content:
            self.__process_directory_item(item)

    def __process_directory_item(self, entry: str):
        if entry.startswith('dir'):
            name = entry.replace("dir ", "")

            # Verify existence of folder
            # item = self.__get_item(name)
            item = self.get_item([name])
            # assert item and item.is_directory(), f"Folder {name} not found!"

            if not item:
                if debug_level >= 3:
                    print(f"Creating folder {name}")

                self.create_directory([name])
        else:
            entry = entry.split(" ")
            size = int(entry[0])
            name = entry[1]

            if debug_level >= 3:
                print(f"Adding file {name} (size={size}) to {self.current_path}")

            item = self.get_item(self.current_path)
            assert item and item.is_directory(), f"No folder on path {self.current_path}"

            item.add_file(File(name, size))

    def print(self, **kwargs: Unpack[DirectoryPrintArgs]):
        print(f"- / (dir, size={self.get_size()})")

        super().print(level=1, hide_empty=kwargs.get('hide_empty'))


class Command:
    def __init__(self, name: str, args: List[str]):
        self.name = name
        self.args = args

        self.output = None

    def print(self):
        print(f"{self}")

        if self.output:
            for line in self.output:
                print(f"  {line}")

    def set_output(self, output: List[str]):
        self.output = output

    def __str__(self):
        return f"{self.name} {self.args if self.args else ''}"

    def __repr__(self):
        return self.__str__()


class SeventhDayTask(AdventOfCodeTask):
    def __init__(self):
        self.last_output = []
        self.last_command = None

        self.command_history = []

        self.file_system = FileSystem()

    def run(self):
        data = self.parameters.input[:-1]

        for line in data.split("\n"):
            if line.startswith("$"):
                # Process command
                line = line.replace("$ ", "").split(" ")

                self.parse_command(Command(line[0], line[1:]))
            else:
                # Process output
                self.last_output.append(line)

        self.parse_output()
        self.clean()

        for command in self.command_history:
            # command.print()

            self.process_command(command)

        if debug_level >= 2:
            if debug_level >= 3:
                print("---")

            self.file_system.print(hide_empty=True)

            print("---")

        size = 0

        for item in self.file_system.get_items():
            item_size = item.get_size()

            if item.is_directory() and item_size >= 100_000:
                if debug_level >= 1:
                    print(f"{item.name} (size={item_size})")

                size += item_size

        if debug_level >= 1:
            print("---")
        print(f"Size: {size}")

    def clean(self):
        self.last_output = None
        self.last_command = None

    def parse_command(self, command: Command):
        self.parse_output()

        # print(f"Parsing command: {command}")
        self.last_command = command

        self.command_history.append(command)

    def parse_output(self):
        if self.last_output:
            self.last_command.set_output(self.last_output)

            self.last_output = []

    def process_command(self, command: Command):
        if command.name == 'cd':
            self.file_system.change_directory(command.args[0])
        elif command.name == 'ls':
            assert not command.args, "List directory args not supported!"

            self.file_system.list_directory(command.output)
        else:
            assert "This command is not implemented!"
