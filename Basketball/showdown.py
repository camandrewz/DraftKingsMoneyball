import time
import math
import pandas as pd
from pandas.core.frame import DataFrame
from functools import cmp_to_key
from src import Player
from src import ExpectedValues
from src import Optimization
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelogs

# Download CSV Per Competition and Import it Here
roster = pd.read_csv('Basketball\data\DKSalaries(7).csv')

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

    # if (player[2] == "Trae Young"):
    #    continue

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

    new_player = Player.Player(player[2], player[0], player[5], id, player[3])
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


num_sims = 1000

print("\n")
print("Running ", num_sims, "Monte Carlo Simulations...")

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
    "RECORD",
    "WIN PCT",
    "COST"
])
monte_carlo_results.to_csv(
    'Basketball\output\most_recent_monte_carlo_showdown_lineups.csv')

for lineup in top_lineups:

    lineup.set_monte_carlo_results(
        monte_carlo_results_dict[lineup.signature]["WINS"]/(num_sims * (len(top_lineups) - 1)))

    monte_carlo_results = monte_carlo_results.append({
        "CAPTAIN": lineup.captain.name,
        "UTIL1": lineup.util1.name,
        "UTIL2": lineup.util2.name,
        "UTIL3": lineup.util3.name,
        "UTIL4": lineup.util4.name,
        "UTIL5": lineup.util5.name,
        "WINS": monte_carlo_results_dict[lineup.signature]["WINS"],
        "RECORD": str(monte_carlo_results_dict[lineup.signature]["WINS"]) + "-" + str(monte_carlo_results_dict[lineup.signature]["LOSSES"]) + "-" + str(monte_carlo_results_dict[lineup.signature]["TIES"]),
        "WIN PCT": monte_carlo_results_dict[lineup.signature]["WINS"]/(num_sims * (len(top_lineups) - 1)),
        "COST": lineup.cost
    }, ignore_index=True)

monte_carlo_results = monte_carlo_results.sort_values(
    by=['WIN PCT'], ascending=False, ignore_index=True)

print('\n')
print("Best Peforming Lineups Ranked: \n")
print(monte_carlo_results)

print('\n')
print("Exporting to DrafKings Template...")

draft_kings_lineups = DataFrame(columns=[
    "CPT",
    "UTIL1",
    "UTIL2",
    "UTIL3",
    "UTIL4",
    "UTIL5"
])

num_lineups_wanted = 20


def compare_monte_carlo(lineup1, lineup2):
    return lineup1.monte_carlo_win_pct > lineup2.monte_carlo_win_pct


top_lineups = sorted(top_lineups, key=cmp_to_key(compare_monte_carlo))

for index, lineup in enumerate(top_lineups):

    if index < num_lineups_wanted:

        draft_kings_lineups = draft_kings_lineups.append({
            "CPT": lineup.captain.dk_id,
            "UTIL1": lineup.util1.dk_id,
            "UTIL2": lineup.util2.dk_id,
            "UTIL3": lineup.util3.dk_id,
            "UTIL4": lineup.util4.dk_id,
            "UTIL5": lineup.util5.dk_id
        }, ignore_index=True)


draft_kings_lineups.rename(columns={"UTIL1": "UTIL", "UTIL2": "UTIL",
                           "UTIL3": "UTIL", "UTIL4": "UTIL", "UTIL5": "UTIL"}, inplace=True)

draft_kings_lineups.reset_index(drop=True, inplace=True)

draft_kings_lineups.to_csv(
    'Basketball\output\draftKings_lineups_for_import.csv')

print("\n")
print("All Done!")
