# noinspection PyPackageRequirements
from aoc import AdventOfCodeTask


# https://adventofcode.com/2015/day/2
class SecondDayTask(AdventOfCodeTask):
    def run(self):
        needed_wrapping_paper = 0
        needed_ribbon = 0

        for data in self.task_input.split("\n"):
            # Skip last empty line
            if not data:
                continue

            (length, width, height) = [int(value) for value in data.split("x")]
            bow_ribbon = length * width * height

            # Calculate all 3 sides areas
            first_face_area = length * width
            second_face_area = width * height
            third_face_area = height * length
            # Get area of the smallest side
            smallest_face_area = min(first_face_area, second_face_area, third_face_area)

            # Calculate box surface area
            box_surface_area = 2 * first_face_area + 2 * second_face_area + 2 * third_face_area
            # Sum total needed area, some reserve
            box_total_needed_area = box_surface_area + smallest_face_area

            total_needed_ribbon = bow_ribbon

            needed_wrapping_paper += box_total_needed_area
            needed_ribbon += total_needed_ribbon

        print(f"Needed wrapping paper: {needed_wrapping_paper}, needed ribbon: {needed_ribbon}")
