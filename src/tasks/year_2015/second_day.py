# noinspection PyPackageRequirements
from aoc import AdventOfCodeTask


class PresentFace:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.area = 0

        # Precalculate area
        self.calculate_area()

    def calculate_area(self) -> int:
        if self.area:
            return self.area

        self.area = self.width * self.height

        return self.area


class Present:
    def __init__(self, length: int, width: int, height: int):
        self.first_face = PresentFace(length, width)
        self.second_face = PresentFace(width, height)
        self.third_face = PresentFace(height, length)

        self.surface_area = 0

        # Precalculate surface area
        self.calculate_surface_area()

        self.bow_ribbon_length = length * width * height

    def get_smallest_face(self):
        # Get area of the smallest side
        smallest_face_area = min(self.first_face.area, self.second_face.area, self.third_face.area)

        if smallest_face_area == self.first_face.area:
            return self.first_face
        elif smallest_face_area == self.second_face.area:
            return self.second_face
        elif smallest_face_area == self.third_face.area:
            return self.third_face

    def calculate_surface_area(self) -> int:
        if self.surface_area:
            return self.surface_area

        # Calculate box surface area
        self.surface_area = 2 * self.first_face.area + 2 * self.second_face.area + 2 * self.third_face.area

        return self.surface_area


# https://adventofcode.com/2015/day/2
class SecondDayTask(AdventOfCodeTask):
    def run(self):
        total_needed_wrapping_paper = 0
        total_needed_ribbon = 0

        for data in self.task_input.split("\n"):
            # Skip last empty line
            if not data:
                continue

            (length, width, height) = [int(value) for value in data.split("x")]

            present = Present(length, width, height)
            present_smallest_face = present.get_smallest_face()

            # Sum total needed wrapping paper with some reserve
            present_needed_wrapping_paper = present.surface_area + present_smallest_face.area
            # Sum total needed ribbon for bow and present
            present_needed_ribbon = 2 * present_smallest_face.width + 2 * present_smallest_face.height
            present_total_needed_ribbon = present.bow_ribbon_length + present_needed_ribbon

            total_needed_wrapping_paper += present_needed_wrapping_paper
            total_needed_ribbon += present_total_needed_ribbon

        print(f"Needed wrapping paper: {total_needed_wrapping_paper}, needed ribbon: {total_needed_ribbon}")
