from builtins import set
from enum import Enum
from typing import Optional

# noinspection PyPackageRequirements
from aoc import AdventOfCodeTask


class Direction(Enum):
    Top = 0
    Left = 1
    Bottom = 2
    Right = 3


class Tree:
    def __init__(self, x: int, y: int, height: int):
        self.x = x
        self.y = y
        self.height = height
        self.visible = None

    def set_visible(self, visible: bool):
        self.visible = visible


class TreeGrid:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.trees = []

    def parse(self, data: str):
        rows = data.split("\n")
        width = 0
        height = 0

        for y in range(len(rows)):
            height = max(height, y)
            row = rows[y]

            for x in range(len(row)):
                width = max(width, x)
                tree_height = int(row[x])

                self.trees.append(Tree(x, y, tree_height))

        self.width = width
        self.height = height

    def test_trees(self):
        # Top, Bottom edges should be always visible
        for x in range(self.width + 1):
            for y in range(2):
                self.get_tree(x, y * self.height).set_visible(True)

        # Left, Right edges should be always visible
        for y in range(self.height + 1):
            for x in range(2):
                self.get_tree(x * self.width, y).set_visible(True)

        for y in range(1, self.height):
            for x in range(1, self.width):
                tree = self.get_tree(x, y)  # TODO: Optimize, function get_tree is called twice!
                visible = self.is_tree_visible(x, y)

                tree.set_visible(visible)

    def print(self, visibility: bool = False):
        last_y = 0

        for tree in self.trees:
            if last_y != tree.y:
                last_y = tree.y

                print()

            if visibility:
                if tree.visible is None:
                    text = "u"
                elif tree.visible:
                    text = "y"
                else:
                    text = "n"
            else:
                text = tree.height

            # ('y' if tree.visible else 'n') if visibility else tree.height
            print(text, end="")

        print()

    def get_trees(self):
        return self.trees

    def get_tree(self, x: int, y: int) -> Optional[Tree]:
        for tree in self.trees:
            if tree.x == x and tree.y == y:
                return tree

        return None

    def is_tree_visible(self, x: int, y: int) -> bool:
        tree = self.get_tree(x, y)

        visible_from = []
        skip_direction = None

        for x in range(self.width):
            direction = Direction.Left if x < tree.x else (Direction.Right if x > tree.x else None)  # None
            # direction = Direction.Right if x > tree.x else direction

            if not direction or skip_direction == direction:
                continue

            other_tree = self.get_tree(x, tree.y)

            # print(direction)

            if other_tree.height >= tree.height:
                skip_direction = direction

                if visible_from.count(direction) > 0:
                    visible_from.remove(direction)
            else:
                visible_from.append(direction)

        for y in range(self.height):
            direction = Direction.Top if y < tree.y else (Direction.Bottom if y > tree.y else None)  # None
            # direction = Direction.Right if x > tree.x else direction

            if not direction or skip_direction == direction:
                continue

            other_tree = self.get_tree(tree.x, y)

            # print(direction)

            if other_tree.height >= tree.height:
                skip_direction = direction

                if visible_from.count(direction) > 0:
                    visible_from.remove(direction)
            else:
                visible_from.append(direction)

        return len(visible_from) > 0


class EighthDayTask(AdventOfCodeTask):
    def __init__(self):
        self.grid = TreeGrid()

    def run(self):
        data = self.parameters.input[:-1]
        self.grid.parse(data)

        print("Calculating tree visibility...")
        self.grid.test_trees()
        print("---")

        # self.grid.print()
        # print("---")
        self.grid.print(True)

        visible_trees = sum([1 for tree in self.grid.get_trees() if tree.visible])

        print("---")
        print(f"Visible trees: {visible_trees}")

        # self.grid.test_trees()
        # print(self.grid.is_tree_visible(1, 1))
