import time
import math
import pandas as pd
from pandas.core.frame import DataFrame
from src import Player
from src import ExpectedValues
from src import Optimization
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelogs

# Download CSV Per Competition and Import it Here
roster = pd.read_csv('Basketball\data\DKSalaries(4).csv')

# Iterate through rows adding each player to a list of player objects 'all_players'
print("Processing CSV file...")
all_players = []

for player in roster.values:

    '''
    Data Index Key

    0 = Position
    1 = NAME + ID
    2 = NAME
    3 = ID
    4 = CPT or UTIL
    5 = Salary
    6 = Event NAME
    '''

    if (player[4] == 'CPT'):
        continue

    if (player[2] == "Trae Young"):
        continue

    if (player[2] == "Brandon Goodwin"):
        continue

    if (player[2] == "Donte DiVincenzo"):
        continue

    if (player[2] == "De'Andre Hunter"):
        continue

    if (player[2] == "Patrick Patterson"):
        continue

    if (player[2] == "Serge Ibaka"):
        continue

    if (player[2] == "Kawhi Leonard"):
        continue

    if (player[2] == "Giannis Antetokounmpo"):
        continue

    player_api = players.find_players_by_full_name(player[2])

    if (player_api == []):
        continue
    else:
        id = player_api[0]['id']

    new_player = Player.Player(player[2], player[0], player[5], id)
    all_players.append(new_player)


'''
Statistics we care about for DraftKings DFS

Points: +1 for each
3pt Shot Made: +.5
Rebound: +1.25
Assist: +1.5
Steal: +2
Block: +2
Turnover: -.5
Double-Double: +1.5
Triple-Double: +3
'''

print("Calculating Expected Values...")

for player in all_players:

    id = player.api_id

    logs = playergamelogs.PlayerGameLogs(
        player_id_nullable=id, season_nullable="2020-21", season_type_nullable="Playoffs", last_n_games_nullable=10)

    df = logs.get_data_frames()

    new_df = DataFrame(columns=[
        "SEASON_YEAR",
        "PLAYER_ID",
        "PLAYER_NAME",
        "GAME_ID",
        "MIN",
        "FG3M",
        "REB",
        "AST",
        "TOV",
        "STL",
        "BLK",
        "PTS",
    ])

    global team_id

    for game in df[0].values:

        team_id = game[4]

        new_df = new_df.append({
            "SEASON_YEAR": game[0],
            "PLAYER_ID": game[1],
            "PLAYER_NAME": game[2],
            "GAME_ID": game[7],
            "MIN": game[11],
            "FG3M": game[15],
            "REB": game[23],
            "AST": game[24],
            "TOV": game[25],
            "STL": game[26],
            "BLK": game[27],
            "PTS": game[31]
        }, ignore_index=True)

    ExpectedValues.calculate_threes(player, new_df)
    ExpectedValues.calculate_pts(player, new_df)
    ExpectedValues.calculate_rebounds(player, new_df)
    ExpectedValues.calculate_assists(player, new_df)
    ExpectedValues.calculate_steals(player, new_df)
    ExpectedValues.calculate_blocks(player, new_df)
    ExpectedValues.calculate_turnovers(player, new_df)
    ExpectedValues.calculate_minutes(player, new_df, team_id)
    player.set_doubles()
    player.set_expected_fantasy_points()

    time.sleep(.600)


final_dataFrame = DataFrame(columns=[
    "PLAYER_NAME",
    "POS",
    "FG3M",
    "REB",
    "AST",
    "TOV",
    "STL",
    "BLK",
    "PTS",
    "DD",
    "TD",
    "SALARY",
    "PRJ"
])


for player in all_players:

    salary = 0

    for roster_entry in roster.values:
        if (roster_entry[2] == player.name):
            salary = roster_entry[5]

    final_dataFrame = final_dataFrame.append({
        "PLAYER_NAME": player.name,
        "POS": player.position,
        "FG3M": player.expected_3pm,
        "REB": player.expected_rebounds,
        "AST": player.expected_assists,
        "TOV": player.expected_turnovers,
        "STL": player.expected_steals,
        "BLK": player.expected_blocks,
        "PTS": player.expected_pts,
        "DD": player.double_double,
        "TD": player.triple_double,
        "SALARY": salary,
        "PRJ": player.expected_fantasy_points,
        "MINUTES": player.expected_minutes,
        "PRJ*MIN": ((player.expected_minutes * player.expected_fantasy_points)/1000)
    }, ignore_index=True)

final_dataFrame = final_dataFrame.sort_values(
    by=['PRJ'], ascending=False, ignore_index=True)

print("All Expected Values: \n")
final_dataFrame.to_csv(
    'Basketball\output\most_recent_showdown_projections.csv')
print(final_dataFrame)


top_lineups = Optimization.create_best_lineups_showdown(all_players)

results = DataFrame(columns=[
    "CAPTAIN",
    "UTIL1",
    "UTIL2",
    "UTIL3",
    "UTIL4",
    "UTIL5",
    "PRJ",
    # "PRJ*MIN",
    "COST"
])

for lineup in top_lineups:
    results = results.append({
        "CAPTAIN": lineup.captain.name,
        "UTIL1": lineup.util1.name,
        "UTIL2": lineup.util2.name,
        "UTIL3": lineup.util3.name,
        "UTIL4": lineup.util4.name,
        "UTIL5": lineup.util5.name,
        "PRJ": lineup.projection,
        # "PRJ*MIN": lineup.get("PRJ*MIN"),
        "COST": lineup.cost
    }, ignore_index=True)

print('\n')
print("Best Lineups Ranked: \n")
results.to_csv('Basketball\output\most_recent_best_showdown_lineups.csv')
print(results)

print("\n")
print("Running 10,000 Monte Carlo Simulation...")

num_sims = 1000

monte_carlo_results_dict = Optimization.monte_carlo_simulations(
    top_lineups, num_sims)

monte_carlo_results = DataFrame(columns=[
    "CAPTAIN",
    "UTIL1",
    "UTIL2",
    "UTIL3",
    "UTIL4",
    "UTIL5",
    "WINS",
    "WIN PCT",
    "COST"
])

for lineup in top_lineups:
    monte_carlo_results = monte_carlo_results.append({
        "CAPTAIN": lineup.captain.name,
        "UTIL1": lineup.util1.name,
        "UTIL2": lineup.util2.name,
        "UTIL3": lineup.util3.name,
        "UTIL4": lineup.util4.name,
        "UTIL5": lineup.util5.name,
        "WINS": monte_carlo_results_dict[lineup.signature],
        "WIN PCT": monte_carlo_results_dict[lineup.signature]/(num_sims * (len(top_lineups) - 1)),
        "COST": lineup.cost
    }, ignore_index=True)

monte_carlo_results = monte_carlo_results.sort_values(
    by=['WIN PCT'], ascending=False, ignore_index=True)

print('\n')
print("Best Peforming Lineups Ranked: \n")
print(monte_carlo_results)
