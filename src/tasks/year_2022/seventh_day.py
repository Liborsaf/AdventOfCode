from __future__ import annotations

from typing import List, Optional, TypedDict
from typing_extensions import Unpack

# noinspection PyPackageRequirements
from aoc import AdventOfCodeTask

# TODO: This task is big mess and needs cleanup someday


debug_level = 0  # (0), [1], 2, 3
debug_empty_directories = False


class DirectoryPrintArgs(TypedDict):
    level: int
    hide_empty: bool


class DirectoryTreePrintArgs(TypedDict):
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

        return directory

    def __get_item(self, name: str) -> Optional[File | Directory]:
        for item in self.content:
            if item.name == name:
                return item

        return None

    def fetch_directory_tree(self, directories: List[Directory]):
        for item in self.get_items():
            if item.is_directory():
                directories.append(item)

                item.fetch_directory_tree(directories)

    def get_items(self):
        return self.content

    def calculate_size(self) -> int:
        self.size = self.get_size()

        return self.size

    def get_size(self) -> int:
        size = super().get_size()

        if size > 0:
            return size

        for item in self.content:
            size += item.get_size()

        return size

    def is_directory(self) -> bool:
        return True


class FileSystem(Directory):
    def __init__(self):
        super().__init__('/')

        self.current_path = []
        self.directory_tree = []

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

    def build_directory_tree(self):
        self.fetch_directory_tree(self.directory_tree)

        for directory in self.directory_tree:
            directory.calculate_size()

        # Sort directory tree
        self.directory_tree = sorted(self.directory_tree, key=lambda directory_: directory_.get_size())  # reverse=True

    def print(self, **kwargs: Unpack[DirectoryPrintArgs]):
        print(f"- / (dir, size={self.get_size()})")

        super().print(level=1, hide_empty=kwargs.get('hide_empty'))

    def print_directory_tree(self, **kwargs: Unpack[DirectoryTreePrintArgs]):
        kwargs.setdefault('hide_empty', False)
        hide_empty = kwargs.get('hide_empty')

        for directory in self.directory_tree:
            directory_size = directory.get_size()

            if directory_size > 0 or (directory_size == 0 and not hide_empty):
                print(f"{directory.name} (size={directory.get_size()})")

    def get_directory_tree(self):
        return self.directory_tree


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

        self.file_system.build_directory_tree()

        if debug_level >= 2:
            if debug_level >= 3:
                print("---")

            self.file_system.print(hide_empty=not debug_empty_directories)

            print("---")

        if debug_level >= 1:
            self.file_system.print_directory_tree(hide_empty=not debug_empty_directories)

            print("---")

        max_disk_space = 70000000
        needed_update_space = 30000000
        currently_used_space = self.file_system.get_size()
        currently_available_space = max_disk_space - currently_used_space

        needed_to_clean_space = needed_update_space - currently_available_space

        if debug_level >= 1:
            print(f"Max disk space: {max_disk_space}")
            print(f"Needed update space: {needed_update_space}, to clean space: {needed_to_clean_space}")
            print(f"Currently used space: {currently_used_space}, available space: {currently_available_space}")
            print("---")

        size = 0
        needed_directory_size = 0

        for directory in self.file_system.get_directory_tree():
            directory_size = directory.get_size()

            if directory_size <= 100_000:
                size += directory_size

            if directory_size >= needed_to_clean_space and needed_directory_size == 0:
                needed_directory_size = directory_size

        print(f"Size: {size}")
        print(f"Needed directory size to remove: {needed_directory_size}")

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
