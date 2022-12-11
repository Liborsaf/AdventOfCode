from __future__ import annotations

from typing import List, Tuple, Optional

from tkinter import *
# noinspection PyPackageRequirements
from aoc import AdventOfCodeTask


class Vector:
    def __init__(self, x: int = 0, y: Optional[int] = None):
        if not y:
            y = x

        self.x = x
        self.y = y

    def copy(self) -> Vector:
        return Vector(self.x, self.y)

    def __add__(self, other: Vector) -> Vector:
        self.x += other.x
        self.y += other.y

        return self

    # def __sub__(self, other: Vector) -> Vector:
    #    self.x -= other.x
    #    self.y -= other.y
    #
    #    return self

    # def __abs__(self) -> Vector:
    #    self.x = abs(self.x)
    #     self.y = abs(self.y)
    #
    #    return self

    def __mul__(self, other: int | Vector) -> Vector:
        if isinstance(other, int):
            self.x *= other
            self.y *= other
        elif isinstance(other, Vector):
            self.x *= other.x
            self.y *= other.y

        return self

    def __repr__(self):
        return f"V({self.x}, {self.y})"


class Rope:
    def __init__(self):
        self.head_coords = Vector()
        self.tail_coords = self.head_coords.copy()

        self.history = []

    def move(self, vector: Vector, count: int):
        for i in range(count):
            self.head_coords += vector
            self.history.append(('head', self.head_coords.copy()))

        while abs(delta_x := self.head_coords.x - self.tail_coords.x) >= 2:
            self.tail_coords.x += delta_x
            self.history.append(('tail', self.tail_coords.copy()))

        while abs(delta_y := self.head_coords.y - self.tail_coords.y) >= 2:
            self.tail_coords.y += delta_y
            self.history.append(('tail', self.tail_coords.copy()))


class NinthDayTask(AdventOfCodeTask):
    move_vector = {
        'U': Vector(0, 1),
        'D': Vector(0, -1),
        'L': Vector(-1, 0),
        'R': Vector(1, 0)
    }

    def __init__(self):
        self.rope = Rope()
        self.window = None

    def run(self):
        steps = self.parse_steps(self.parameters.input[:-1])

        # print(steps)

        for step in steps:
            self.process_step(step)

        width = 0
        height = 0

        for step in self.rope.history:
            (_, coords) = step

            width = max(width, coords.x)
            height = max(height, coords.y)

        self.window = Window(Vector(width * 3, height * 3))
        self.window.steps_history = self.rope.history

        self.window.run()

    def parse_steps(self, data: str) -> List[Tuple[int, Vector]]:
        steps = []

        for line in data.split("\n"):
            line = line.split(" ")

            step = (int(line[1]), self.move_vector[line[0]])
            steps.append(step)

        return steps

    def process_step(self, step: Tuple[int, Vector]):
        (count, vector) = step

        self.rope.move(vector, count)


class Window:
    pixel_size = 10
    playback_speed = 250

    def __init__(self, size: Vector):
        self.size = size
        self.root = None
        self.canvas = None

        self.index = 0
        self.steps_history = []
        self.last_head_coords = None
        self.last_tail_coords = None

        self.setup_root()
        self.setup_canvas()

    def setup_root(self):
        self.root = Tk()
        self.root.geometry(f"{self.size.x}x{self.size.y}")
        self.root.resizable(False, False)
        self.root.config(bg="black")

    def setup_canvas(self):
        self.canvas = Canvas(self.root, width=self.size.x, height=self.size.y, bg="white")
        self.canvas.pack()

    def run(self):
        self.root.after(self.playback_speed, self.loop)
        self.root.mainloop()

    def loop(self):
        self.canvas.delete("all")

        (node, coords) = self.steps_history[self.index]

        if node == 'head':
            self.last_head_coords = coords
        elif node == 'tail':
            self.last_tail_coords = coords

        if self.last_head_coords:
            self.draw(self.last_head_coords, "green")

        if self.last_tail_coords:
            self.draw(self.last_tail_coords, "red")

        self.index += 1

        self.root.after(self.playback_speed, self.loop)

    def draw(self, coords: Vector, color: str, size: Vector = Vector(pixel_size)):

        coords *= self.pixel_size

        coords.x += self.size.x // 2
        coords.y += self.size.y // 2

        # print(coords)

        self.canvas.create_rectangle(coords.x, coords.y, coords.x + size.x, coords.y + size.y, fill=color)
