from enum import Enum
from typing import Optional, List

from aoc import AdventOfCodeTask


class FirstDayTask(AdventOfCodeTask):
    def run(self):
        elves = self.sum_elves()

        sorted_elves = sorted(elves, reverse=True)

        most_elf = sorted_elves[0]
        most_three_elves = sum(sorted_elves[:3])

        print(f"Most elf total: {most_elf}, Most 3 elves total: {most_three_elves}")

    def sum_elves(self) -> List[int]:
        elves = []
        elf_calories = 0

        for data in self.input.split("\n"):
            if data == '':
                elves.append(elf_calories)
                elf_calories = 0

                continue

            elf_calories += int(data)

        return elves


class SecondDayTask(AdventOfCodeTask):
    class Thing(Enum):
        Rock = 0
        Paper = 1
        Scissors = 2

    class Round(Enum):
        Lose = 0
        Draw = 1
        Win = 2

    opponent_mapping = {
        'A': Thing.Rock,
        'B': Thing.Paper,
        'C': Thing.Scissors
    }

    player_mapping = {
        'X': Thing.Rock,
        'Y': Thing.Paper,
        'Z': Thing.Scissors
    }

    player_mapping_needs = {
        'X': Round.Lose,
        'Y': Round.Draw,
        'Z': Round.Win
    }

    win_strategy = {
        Thing.Rock: Thing.Scissors,
        Thing.Scissors: Thing.Paper,
        Thing.Paper: Thing.Rock
    }

    points_mapping = {
        Thing.Rock: 1,
        Thing.Paper: 2,
        Thing.Scissors: 3
    }

    def run(self):
        points = 0
        second_points = 0

        for data in self.input.split("\n"):
            # Skip last empty line
            if not data:
                continue

            opponent = self.opponent_mapping[data[0]]
            player = self.player_mapping[data[2]]
            player_needs = self.player_mapping_needs[data[2]]

            points += self.calculate_points(player, opponent)

            player = self.figure_thing(opponent, player_needs)
            self.test(player, opponent, player_needs)

            second_points += self.calculate_points(player, opponent)

        print(f"Total points: {points}, Total second points: {second_points}")

    def figure_thing(self, opponent: Thing, player_needs: Round) -> Optional[Thing]:
        player = None

        opponent_win_strategy = self.win_strategy[opponent]

        if player_needs == self.Round.Draw:
            player = opponent
        else:
            for value in self.win_strategy.keys():
                if value == opponent:
                    continue
                elif (player_needs == self.Round.Win and value != opponent_win_strategy) or \
                        (player_needs == self.Round.Lose and value == opponent_win_strategy):
                    player = value

                    break

        return player

    def test(self, player: Thing, opponent: Thing, player_needs: Round):
        if player == opponent:
            test_needs = self.Round.Draw
        elif self.win_strategy[player] == opponent:
            test_needs = self.Round.Win
        else:
            test_needs = self.Round.Lose

        if test_needs != player_needs:
            print(f"Opponent: {opponent}, player: {player}, needs: {player_needs}")

    def calculate_points(self, player: Thing, opponent: Thing) -> int:
        points = self.points_mapping[player]

        if opponent == player:
            # Draw
            points += 3
        elif self.win_strategy[player] == opponent:
            # Win
            points += 6
        else:
            # Lose
            points += 0

        return points
