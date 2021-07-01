import time
import pandas as pd
from pandas.core.frame import DataFrame
from src import Player
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelogs
from nba_api.stats.endpoints import commonplayerinfo
from operator import itemgetter

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

print("Gathering player data...")

for player in all_players:
    id = player.api_id

    if (id == -1):
        continue

    if (player.name == "Trae Young"):
        continue

    if (player.name == "Brandon Goodwin"):
        continue

    if (player.name == "Donte DiVincenzo"):
        continue

    if (player.name == "De'Andre Hunter"):
        continue

    if (player.name == "Patrick Patterson"):
        continue

    if (player.name == "Serge Ibaka"):
        continue

    if (player.name == "Kawhi Leonard"):
        continue

    logs = playergamelogs.PlayerGameLogs(
        player_id_nullable=id, season_nullable="2020-21", season_type_nullable="Playoffs", last_n_games_nullable=10)

    df = logs.get_data_frames()

    global team_id

    last_game = df[0].values[0]
    last_FG3M = last_game[15]
    last_REB = last_game[23]
    last_AST = last_game[24]
    last_TOV = last_game[25]
    last_STL = last_game[26]
    last_BLK = last_game[27]
    last_PTS = last_game[31]

    last_DD = False
    last_TD = False

    doubles = 0

    if (last_PTS >= 10):
        doubles += 1

    if (last_REB >= 10):
        doubles += 1

    if (last_AST >= 10):
        doubles += 1

    if (last_STL >= 10):
        doubles += 1

    if (last_BLK >= 10):
        doubles += 1

    if (doubles >= 3):
        last_TD = True
        last_DD = True
    elif (doubles == 2):
        last_TD = False
        last_DD = True
    else:
        last_TD = False
        last_DD = False

    total_fantasy_points = 0

    total_fantasy_points += 1 * last_PTS
    total_fantasy_points += .5 * last_FG3M
    total_fantasy_points += 1.25 * last_REB
    total_fantasy_points += 1.5 * last_AST
    total_fantasy_points += 2 * last_STL
    total_fantasy_points += 2 * last_BLK
    total_fantasy_points -= .5 * last_TOV

    if (total_fantasy_points < 10):
        time.sleep(.600)
        continue

    for roster_entry in roster.values:
        if (roster_entry[2] == player.name):
            salary = roster_entry[5]

    final_dataFrame = final_dataFrame.append({
        "PLAYER_NAME": player.name,
        "POS": player.position,
        "FG3M": last_FG3M,
        "REB": last_REB,
        "AST": last_AST,
        "TOV": last_TOV,
        "STL": last_STL,
        "BLK": last_BLK,
        "PTS": last_PTS,
        "DD": last_DD,
        "TD": last_TD,
        "SALARY": salary,
        "PRJ": total_fantasy_points
    }, ignore_index=True)

    if ("PG" in player.position):
        point_guards = point_guards.append({
            "PLAYER_NAME": player.name,
            "POS": player.position,
            "FG3M": last_FG3M,
            "REB": last_REB,
            "AST": last_AST,
            "TOV": last_TOV,
            "STL": last_STL,
            "BLK": last_BLK,
            "PTS": last_PTS,
            "DD": last_DD,
            "TD": last_TD,
            "SALARY": salary,
            "PRJ": total_fantasy_points
        }, ignore_index=True)

        all_guards = all_guards.append({
            "PLAYER_NAME": player.name,
            "POS": player.position,
            "FG3M": last_FG3M,
            "REB": last_REB,
            "AST": last_AST,
            "TOV": last_TOV,
            "STL": last_STL,
            "BLK": last_BLK,
            "PTS": last_PTS,
            "DD": last_DD,
            "TD": last_TD,
            "SALARY": salary,
            "PRJ": total_fantasy_points
        }, ignore_index=True)

    if ("SG" in player.position):
        shooting_guards = shooting_guards.append({
            "PLAYER_NAME": player.name,
            "POS": player.position,
            "FG3M": last_FG3M,
            "REB": last_REB,
            "AST": last_AST,
            "TOV": last_TOV,
            "STL": last_STL,
            "BLK": last_BLK,
            "PTS": last_PTS,
            "DD": last_DD,
            "TD": last_TD,
            "SALARY": salary,
            "PRJ": total_fantasy_points
        }, ignore_index=True)

        all_guards = all_guards.append({
            "PLAYER_NAME": player.name,
            "POS": player.position,
            "FG3M": last_FG3M,
            "REB": last_REB,
            "AST": last_AST,
            "TOV": last_TOV,
            "STL": last_STL,
            "BLK": last_BLK,
            "PTS": last_PTS,
            "DD": last_DD,
            "TD": last_TD,
            "SALARY": salary,
            "PRJ": total_fantasy_points
        }, ignore_index=True)

    if ("SF" in player.position):
        small_forwards = small_forwards.append({
            "PLAYER_NAME": player.name,
            "POS": player.position,
            "FG3M": last_FG3M,
            "REB": last_REB,
            "AST": last_AST,
            "TOV": last_TOV,
            "STL": last_STL,
            "BLK": last_BLK,
            "PTS": last_PTS,
            "DD": last_DD,
            "TD": last_TD,
            "SALARY": salary,
            "PRJ": total_fantasy_points
        }, ignore_index=True)

        all_forwards = all_forwards.append({
            "PLAYER_NAME": player.name,
            "POS": player.position,
            "FG3M": last_FG3M,
            "REB": last_REB,
            "AST": last_AST,
            "TOV": last_TOV,
            "STL": last_STL,
            "BLK": last_BLK,
            "PTS": last_PTS,
            "DD": last_DD,
            "TD": last_TD,
            "SALARY": salary,
            "PRJ": total_fantasy_points
        }, ignore_index=True)

    if ("PF" in player.position):
        power_forwards = power_forwards.append({
            "PLAYER_NAME": player.name,
            "POS": player.position,
            "FG3M": last_FG3M,
            "REB": last_REB,
            "AST": last_AST,
            "TOV": last_TOV,
            "STL": last_STL,
            "BLK": last_BLK,
            "PTS": last_PTS,
            "DD": last_DD,
            "TD": last_TD,
            "SALARY": salary,
            "PRJ": total_fantasy_points
        }, ignore_index=True)

        all_forwards = all_forwards.append({
            "PLAYER_NAME": player.name,
            "POS": player.position,
            "FG3M": last_FG3M,
            "REB": last_REB,
            "AST": last_AST,
            "TOV": last_TOV,
            "STL": last_STL,
            "BLK": last_BLK,
            "PTS": last_PTS,
            "DD": last_DD,
            "TD": last_TD,
            "SALARY": salary,
            "PRJ": total_fantasy_points
        }, ignore_index=True)

    if ("C" in player.position):
        centers = centers.append({
            "PLAYER_NAME": player.name,
            "POS": player.position,
            "FG3M": last_FG3M,
            "REB": last_REB,
            "AST": last_AST,
            "TOV": last_TOV,
            "STL": last_STL,
            "BLK": last_BLK,
            "PTS": last_PTS,
            "DD": last_DD,
            "TD": last_TD,
            "SALARY": salary,
            "PRJ": total_fantasy_points
        }, ignore_index=True)

        all_forwards = all_forwards.append({
            "PLAYER_NAME": player.name,
            "POS": player.position,
            "FG3M": last_FG3M,
            "REB": last_REB,
            "AST": last_AST,
            "TOV": last_TOV,
            "STL": last_STL,
            "BLK": last_BLK,
            "PTS": last_PTS,
            "DD": last_DD,
            "TD": last_TD,
            "SALARY": salary,
            "PRJ": total_fantasy_points
        }, ignore_index=True)

    time.sleep(.600)


print(final_dataFrame)


def check_lineup_for_player(lineup, name):
    for key in lineup.keys():
        if (key != "PRJ" and key != "COST" and key != "PRJ*MIN"):
            if (lineup.get(key).get("NAME") == name):
                return True

    return False


def create_best_lineups():

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
        "COST"
    ])

    print("Creating Lineups...")

    total_combos = (len(point_guards.values) * len(shooting_guards.values) * len(small_forwards.values)

                    * len(power_forwards.values) * len(centers.values) * len(all_guards.values) *

                    len(all_forwards.values) * len(final_dataFrame.values))

    print("Total Combinations: ", total_combos)

    for pg in point_guards.values:

        current_lineup = {"PG": {}, "SG": {}, "SF": {}, "PF": {}, "C": {
        }, "GUARD": {}, "FORWARD": {}, "UTIL": {}, "PRJ": 0, "COST": 0}

        if (check_lineup_for_player(current_lineup, pg[0])):
            continue

        details = {"NAME": pg[0], "PRJ": pg[12], "SALARY": pg[11]}
        current_lineup["PG"] = details
        current_lineup["PRJ"] = pg[12]
        current_lineup["COST"] = pg[11]

        if current_lineup.get("COST") > 50000:
            continue

        for sg in shooting_guards.values:

            if (check_lineup_for_player(current_lineup, sg[0])):
                continue

            details = {"NAME": sg[0], "PRJ": sg[12], "SALARY": sg[11]}
            current_lineup["SG"] = details
            current_lineup["PRJ"] = pg[12] + sg[12]
            current_lineup["COST"] = pg[11] + sg[11]

            if current_lineup.get("COST") > 50000:
                continue

            for sf in small_forwards.values:

                if (check_lineup_for_player(current_lineup, sf[0])):
                    continue

                details = {"NAME": sf[0], "PRJ": sf[12], "SALARY": sf[11]}
                current_lineup["SF"] = details
                current_lineup["PRJ"] = pg[12] + sg[12] + sf[12]
                current_lineup["COST"] = pg[11] + sg[11] + sf[11]

                if current_lineup.get("COST") > 50000:
                    continue

                for pf in power_forwards.values:

                    if (check_lineup_for_player(current_lineup, pf[0])):
                        continue

                    details = {"NAME": pf[0], "PRJ": pf[12], "SALARY": pf[11]}
                    current_lineup["PF"] = details
                    current_lineup["PRJ"] = pg[12] + sg[12] + sf[12] + pf[12]
                    current_lineup["COST"] = pg[11] + sg[11] + sf[11] + pf[11]

                    if current_lineup.get("COST") > 50000:
                        continue

                    for center in centers.values:

                        if (check_lineup_for_player(current_lineup, center[0])):
                            continue

                        details = {
                            "NAME": center[0], "PRJ": center[12], "SALARY": center[11]}
                        current_lineup["C"] = details

                        current_lineup["PRJ"] = pg[12] + \
                            sg[12] + sf[12] + pf[12] + center[12]
                        current_lineup["COST"] = pg[11] + \
                            sg[11] + sf[11] + pf[11] + center[11]

                        if current_lineup.get("COST") > 50000:
                            continue

                        for guard in all_guards.values:

                            if (check_lineup_for_player(current_lineup, guard[0])):
                                continue

                            details = {
                                "NAME": guard[0], "PRJ": guard[12], "SALARY": guard[11]}
                            current_lineup["GUARD"] = details

                            current_lineup["PRJ"] = pg[12] + sg[12] + \
                                sf[12] + pf[12] + center[12] + guard[12]
                            current_lineup["COST"] = pg[11] + sg[11] + \
                                sf[11] + pf[11] + center[11] + guard[12]

                            if current_lineup.get("COST") > 50000:
                                continue

                            for forward in all_forwards.values:

                                if (check_lineup_for_player(current_lineup, forward[0])):
                                    continue

                                details = {
                                    "NAME": forward[0], "PRJ": forward[12], "SALARY": forward[11]}
                                current_lineup["FORWARD"] = details

                                current_lineup["PRJ"] = pg[12] + sg[12] + sf[12] + \
                                    pf[12] + center[12] + \
                                    guard[12] + forward[12]
                                current_lineup["COST"] = pg[11] + sg[11] + sf[11] + \
                                    pf[11] + center[11] + \
                                    guard[11] + forward[11]

                                if current_lineup.get("COST") > 50000:
                                    continue

                                for util in final_dataFrame.values:

                                    if (check_lineup_for_player(current_lineup, util[0])):
                                        continue

                                    details = {
                                        "NAME": util[0], "PRJ": util[12], "SALARY": util[11]}
                                    current_lineup["UTIL"] = details

                                    current_lineup["PRJ"] = pg[12] + sg[12] + sf[12] + \
                                        pf[12] + center[12] + \
                                        guard[12] + forward[12] + util[12]
                                    current_lineup["COST"] = pg[11] + sg[11] + sf[11] + \
                                        pf[11] + center[11] + \
                                        guard[11] + forward[11] + util[11]

                                    if current_lineup.get("COST") > 50000:
                                        continue

                                    lineup_score = current_lineup.get("PRJ")
                                    lineup_cost = current_lineup.get("COST")

                                    if lineup_score > 300 and lineup_cost < 50000:
                                        results = results.append({
                                            "PG": current_lineup.get("PG").get("NAME"),
                                            "SG": current_lineup.get("SG").get("NAME"),
                                            "SF": current_lineup.get("SF").get("NAME"),
                                            "PF": current_lineup.get("PF").get("NAME"),
                                            "C": current_lineup.get("C").get("NAME"),
                                            "GUARD": current_lineup.get("GUARD").get("NAME"),
                                            "FORWARD": current_lineup.get("FORWARD").get("NAME"),
                                            "UTIL": current_lineup.get("UTIL").get("UTIL"),
                                            "PRJ": current_lineup.get("PRJ"),
                                            "COST": current_lineup.get("COST")
                                        }, ignore_index=True)

    print("Now we sort")

    results = results.sort_values(
        by=['PRJ'], ascending=False, ignore_index=True)

    return results


results = create_best_lineups()

print('\n')
print("Best Lineups Ranked: \n")
print(results.head(10))
