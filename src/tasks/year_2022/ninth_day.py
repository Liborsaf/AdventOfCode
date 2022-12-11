from enum import Enum
from typing import List, Tuple

from tkinter import *
# noinspection PyPackageRequirements
from aoc import AdventOfCodeTask


class Direction(Enum):
    Up = 0,
    Down = 1,
    Left = 2,
    Right = 3


class Node:
    def __init__(self):
        self.x = 0
        self.y = 0


class NinthDayTask(AdventOfCodeTask):
    direction_mapping = {
        'U': Direction.Up,
        'D': Direction.Down,
        'L': Direction.Left,
        'R': Direction.Right
    }

    pixel_size = 10

    def __init__(self):
        self.head = Node()
        self.tail = Node()

        self.head_index = 0
        self.tail_index = 0

        self.step_history = []
        self.tail_history = []

        self.index = 0

        self.root = None
        self.canvas = None

        self.head_coords = []
        self.tail_coords = []

    def run(self):
        data = self.parameters.input[:-1]

        steps = self.parse_steps(data)

        for (direction, count) in steps:
            if direction == Direction.Up:
                self.head.y += count
            elif direction == Direction.Down:
                self.head.y -= count
            elif direction == Direction.Left:
                self.head.x += count
            elif direction == Direction.Right:
                self.head.x -= count

            self.step_history.append(('head', (self.head.x, self.head.y)))

            self.process_tail()

        self.width = max([i[1][0] * self.pixel_size for i in self.step_history])
        self.height = max([i[1][1] * self.pixel_size for i in self.step_history])

        print(f"{self.width}x{self.height}")

        self.root = Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.config(bg="#000")

        self.canvas = Canvas(self.root, width=self.width, height=self.height, bg="#fff")
        self.canvas.pack()

        self.root.after(500, self.step)
        self.root.mainloop()

    def step(self):
        (what, coords) = self.step_history[self.index]
        (x, y) = coords

        x += self.width // 2
        y += self.height // 2

        x *= self.pixel_size
        y *= self.pixel_size

        if what == 'tail':
            self.tail_coords = (x, y)
        elif what == 'head':
            self.head_coords = (x, y)

        print(f"Step (what={what}, coords={coords})")

        self.canvas.delete("all")

        if self.head_coords:
            self.canvas.create_rectangle(self.head_coords[0], self.head_coords[1],
                                         self.head_coords[0] + self.pixel_size, self.head_coords[1] + self.pixel_size,
                                         fill='green')

        if self.tail_coords:
            self.canvas.create_rectangle(self.tail_coords[0], self.tail_coords[1],
                                         self.tail_coords[0] + self.pixel_size, self.tail_coords[1] + self.pixel_size,
                                         fill='red')

        self.index += 1

        self.root.after(500, self.step)

    def process_tail(self):
        while abs(difference_x := self.head.x - self.tail.x) >= 2:
            self.tail.x += difference_x / abs(difference_x)
            self.tail_history.append((self.tail.x, self.tail.y))
            self.step_history.append(('tail', (self.tail.x, self.tail.y)))

        while abs(difference_y := self.head.y - self.tail.y) >= 2:
            self.tail.y += difference_y / abs(difference_y)
            self.tail_history.append((self.tail.x, self.tail.y))
            self.step_history.append(('tail', (self.tail.x, self.tail.y)))

        while self.tail.x != self.head.x and self.tail.y != self.head.y:
            is_negative_x = (self.head.x - self.tail.x) < 0
            is_negative_y = (self.head.x - self.tail.y) < 0

            self.tail.x += -1 if is_negative_x else 1
            self.tail.y += -1 if is_negative_y else 1

            self.tail_history.append((self.tail.x, self.tail.y))
            self.step_history.append(('tail', (self.tail.x, self.tail.y)))

    def parse_steps(self, data: str) -> List[Tuple[Direction, int]]:
        steps = []

        for line in data.split("\n"):
            line = line.split(" ")

            direction = self.direction_mapping[line[0]]
            count = int(line[1])

            steps.append((direction, count))

        return steps
