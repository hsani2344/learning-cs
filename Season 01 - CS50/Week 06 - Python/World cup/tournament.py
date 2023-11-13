# Simulate a sports tournament

import csv
import sys
import random

# Number of simluations to run
N = 1000


def main():
    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILENAME")

    teams = []
    # Read teams into memory from CSV file
    csvfile = open(sys.argv[1], mode="r", newline="")
    team_dict = csv.DictReader(csvfile)

    counts = {}
    # TODO: Simulate N tournaments and keep track of win counts
    for i in team_dict:
        # DEBUG
        # print(i)
        teams.append(i)
    # DEBUG
    # print(teams)
    # print(counts)
    # print(simulate_tournament(teams))

    for i in range(N):
        winner_team = simulate_tournament(teams)
        if winner_team in counts:
            counts[winner_team] += 1
        else:
            counts[winner_team] = 1

    # Print each team's chances of winning, according to simulation
    for team in sorted(counts, key=lambda team: counts[team], reverse=True):
        print(f"{team}: {counts[team] * 100 / N:.1f}% chance of winning")


def simulate_game(team1, team2):
    """Simulate a game. Return True if team1 wins, False otherwise."""
    rating1 = team1["rating"]
    rating2 = team2["rating"]
    probability = 1 / (1 + 10 ** ((int(rating2) - int(rating1)) / 600))
    return random.random() < probability


def simulate_round(teams):
    """Simulate a round. Return a list of winning teams."""
    winners = []

    # Simulate games for all pairs of teams
    for i in range(0, len(teams), 2):
        if simulate_game(teams[i], teams[i + 1]):
            winners.append(teams[i])
        else:
            winners.append(teams[i + 1])

    return winners


def simulate_tournament(teams):
    """Simulate a tournament. Return name of winning team."""
    # TODO
    remaining_teams = teams
    while len(remaining_teams) > 1:
        remaining_teams = simulate_round(remaining_teams)
    winner = remaining_teams[0]["team"]
    return winner


if __name__ == "__main__":
    main()
