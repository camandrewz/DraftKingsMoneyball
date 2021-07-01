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
roster = pd.read_csv('data\DKSalaries(5).csv')

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
        id = -1
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

    if (id == -1):
        continue

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

    player.set_expected_threes(ExpectedValues.calculate_threes(new_df))
    player.set_expected_pts(ExpectedValues.calculate_pts(new_df))
    player.set_expected_rebounds(ExpectedValues.calculate_rebounds(new_df))
    player.set_expected_assists(ExpectedValues.calculate_assists(new_df))
    player.set_expected_steals(ExpectedValues.calculate_steals(new_df))
    player.set_expected_blocks(ExpectedValues.calculate_blocks(new_df))
    player.set_expected_turnovers(ExpectedValues.calculate_turnovers(new_df))
    player.set_expected_minutes(
        ExpectedValues.calculate_minutes(new_df, team_id))
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
point_guards = DataFrame(columns=[
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
shooting_guards = DataFrame(columns=[
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
small_forwards = DataFrame(columns=[
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
power_forwards = DataFrame(columns=[
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
centers = DataFrame(columns=[
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

all_guards = DataFrame(columns=[
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

all_forwards = DataFrame(columns=[
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

    if (player.api_id == -1):
        continue

    salary = 0

    for roster_entry in roster.values:
        if (roster_entry[2] == player.name):
            salary = roster_entry[5]

    # Don't waste time on anyone projected less than 10 points
    if player.expected_fantasy_points < 10:
        continue

    # Don't waste time on anyone projected less than 15 minutes
    if player.expected_minutes < 15:
        continue

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

    if ("PG" in player.position):
        point_guards = point_guards.append({
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
            "PRJ*MIN": ((player.expected_minutes * player.expected_fantasy_points)/1000)
        }, ignore_index=True)

        all_guards = all_guards.append({
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
            "PRJ*MIN": ((player.expected_minutes * player.expected_fantasy_points)/1000)
        }, ignore_index=True)

    if ("SG" in player.position):
        shooting_guards = shooting_guards.append({
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
            "PRJ*MIN": ((player.expected_minutes * player.expected_fantasy_points)/1000)
        }, ignore_index=True)

        all_guards = all_guards.append({
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
            "PRJ*MIN": ((player.expected_minutes * player.expected_fantasy_points)/1000)
        }, ignore_index=True)

    if ("SF" in player.position):
        small_forwards = small_forwards.append({
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
            "PRJ*MIN": ((player.expected_minutes * player.expected_fantasy_points)/1000)
        }, ignore_index=True)

        all_forwards = all_forwards.append({
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
            "PRJ*MIN": ((player.expected_minutes * player.expected_fantasy_points)/1000)
        }, ignore_index=True)

    if ("PF" in player.position):
        power_forwards = power_forwards.append({
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
            "PRJ*MIN": ((player.expected_minutes * player.expected_fantasy_points)/1000)
        }, ignore_index=True)

        all_forwards = all_forwards.append({
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
            "PRJ*MIN": ((player.expected_minutes * player.expected_fantasy_points)/1000)
        }, ignore_index=True)

    if ("C" in player.position):
        centers = centers.append({
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
            "PRJ*MIN": ((player.expected_minutes * player.expected_fantasy_points)/1000)
        }, ignore_index=True)

final_dataFrame = final_dataFrame.sort_values(
    by=['PRJ*MIN'], ascending=False, ignore_index=True)

print("All Expected Values: \n")
print(final_dataFrame)


def check_lineup_for_player(lineup, name):
    for key in lineup.keys():
        if (key != "PRJ" and key != "COST" and key != "PRJ*MIN"):
            if (lineup.get(key).get("NAME") == name):
                return True

    return False


top_ten = Optimization.create_best_lineups(
    final_dataFrame, point_guards, shooting_guards, small_forwards, power_forwards, centers, all_guards, all_forwards)

results = DataFrame(columns=[
    "PG",
    "SG",
    "SF",
    "PF",
    "C",
    "GUARD",
    "FORWARD",
    "UTIL",
    "PRJ",
    "PRJ*MIN",
    "COST"
])

for lineup in top_ten:
    results = results.append({
        "PG": lineup.get("PG").get("NAME"),
        "SG": lineup.get("SG").get("NAME"),
        "SF": lineup.get("SF").get("NAME"),
        "PF": lineup.get("PF").get("NAME"),
        "C": lineup.get("C").get("NAME"),
        "GUARD": lineup.get("GUARD").get("NAME"),
        "FORWARD": lineup.get("FORWARD").get("NAME"),
        "UTIL": lineup.get("UTIL").get("NAME"),
        "PRJ": lineup.get("PRJ"),
        "PRJ*MIN": lineup.get("PRJ*MIN"),
        "COST": lineup.get("COST")
    }, ignore_index=True)

print('\n')
print("Best Lineups Ranked: \n")
print(results.head(10))
