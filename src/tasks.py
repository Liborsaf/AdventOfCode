from aoc import AdventOfCodeTask


class FirstDayTask(AdventOfCodeTask):
    def run(self):
        elves = []
        elf_calories = 0

        for data in self.input.split("\n"):
            if data == '':
                elves.append(elf_calories)
                elf_calories = 0

                continue

            elf_calories += int(data)

        sorted_elves = sorted(elves, reverse=True);

        most_elf = sorted_elves[0]
        most_three_elves = sum(sorted_elves[:3])

        print(f"Most elf total: {most_elf}, Most 3 elves total: {most_three_elves}")


class SecondDayTask(AdventOfCodeTask):
    opponent_mapping = {
        'A': 'Rock',
        'B': 'Paper',
        'C': 'Scissors'
    }

    player_mapping = {
        'X': 'Rock',
        'Y': 'Paper',
        'Z': 'Scissors'
    }

    player_mapping_needs = {
        'X': 'Lose',
        'Y': 'Draw',
        'Z': 'Win'
    }

    win_strategy = {
        'Rock': 'Scissors',
        'Scissors': 'Paper',
        'Paper': 'Rock'
    }

    points_mapping = {
        'Rock': 1,
        'Paper': 2,
        'Scissors': 3
    }

    def run(self):
        points = 0
        second_points = 0

        for data in self.input.split("\n"):
            if not data:
                continue

            opponent = self.opponent_mapping[data[0]]
            player = self.player_mapping[data[2]]
            player_needs = self.player_mapping_needs[data[2]]

            points += self.calculate_points(player, opponent)

            opponent_win_strategy = self.win_strategy[opponent]

            if player_needs == 'Draw':
                player = opponent
            else:
                for value in self.win_strategy.keys():
                    if value == opponent:
                        continue

                    elif player_needs == 'Win' and value != opponent_win_strategy:
                        player = value

                        break
                    elif player_needs == 'Lose' and value == opponent_win_strategy:
                        player = value

                        break

            if player == opponent:
                test_needs = "Draw"
            elif self.win_strategy[player] == opponent:
                test_needs = "Win"
            else:
                test_needs = "Lose"

            if test_needs != player_needs:
                print(f"Opponent: {opponent}, player: {player}, needs: {player_needs}")

            second_points += self.calculate_points(player, opponent)

        print(f"Total points: {points}, Total second points: {second_points}")

    def calculate_points(self, player, opponent):
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

        # points += self.points_mapping[player]

        return points
