# noinspection PyPackageRequirements
from aoc import AdventOfCodeTask


class PresentFace:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def area(self) -> int:
        return self.width * self.height


class Present:
    def __init__(self, length: int, width: int, height: int):
        self.first_face = PresentFace(length, width)
        self.second_face = PresentFace(width, height)
        self.third_face = PresentFace(height, length)

        self.bow_ribbon_length = length * width * height

    def get_smallest_face(self):
        # Precalculate areas of all sides
        first_face_area = self.first_face.area()
        second_face_area = self.second_face.area()
        third_face_area = self.third_face.area()

        # Get area of the smallest side
        smallest_face_area = min(first_face_area, second_face_area, third_face_area)

        if smallest_face_area == first_face_area:
            return self.first_face
        elif smallest_face_area == second_face_area:
            return self.second_face
        elif smallest_face_area == third_face_area:
            return self.third_face

    def surface_area(self) -> int:
        # Calculate box surface area
        return 2 * self.first_face.area() + 2 * self.second_face.area() + 2 * self.third_face.area()


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
            present_needed_wrapping_paper = present.surface_area() + present_smallest_face.area()
            present_needed_ribbon = present.bow_ribbon_length

            total_needed_wrapping_paper += present_needed_wrapping_paper
            total_needed_ribbon += total_needed_ribbon

        print(f"Needed wrapping paper: {total_needed_wrapping_paper}, needed ribbon: {total_needed_ribbon}")
