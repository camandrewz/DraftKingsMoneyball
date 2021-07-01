import collections
import time
from nba_api.stats.endpoints import teamgamelogs
from nba_api.stats.endpoints import commonplayerinfo


def calculate_threes(df):

    fgm = {}

    for game in df.values:

        if (game[5] in fgm.keys()):
            fgm.update({game[5]: (fgm.get(game[5]) + 1)})
        else:
            fgm.update({game[5]: 1})

    fgm = collections.OrderedDict(sorted(fgm.items()))

    for key in fgm.keys():
        fgm.update({key: (fgm.get(key)/len(df.values))})

    expected_value = 0

    for key in fgm.keys():
        expected_value += (key * fgm.get(key))

    return expected_value


def calculate_pts(df):

    pts = {}

    for game in df.values:

        if (game[11] in pts.keys()):
            pts.update({game[11]: (pts.get(game[11]) + 1)})
        else:
            pts.update({game[11]: 1})

    pts = collections.OrderedDict(sorted(pts.items()))

    for key in pts.keys():
        pts.update({key: (pts.get(key)/len(df.values))})

    expected_pts = 0

    for key in pts.keys():
        expected_pts += (key * pts.get(key))

    return expected_pts


def calculate_rebounds(df):

    rebounds = {}

    for game in df.values:

        if (game[6] in rebounds.keys()):
            rebounds.update({game[6]: (rebounds.get(game[6]) + 1)})
        else:
            rebounds.update({game[6]: 1})

    rebounds = collections.OrderedDict(sorted(rebounds.items()))

    for key in rebounds.keys():
        rebounds.update({key: (rebounds.get(key)/len(df.values))})

    expected_rebounds = 0

    for key in rebounds.keys():
        expected_rebounds += (key * rebounds.get(key))

    return expected_rebounds


def calculate_assists(df):

    assists = {}

    for game in df.values:

        if (game[7] in assists.keys()):
            assists.update({game[7]: (assists.get(game[7]) + 1)})
        else:
            assists.update({game[7]: 1})

    assists = collections.OrderedDict(sorted(assists.items()))

    for key in assists.keys():
        assists.update({key: (assists.get(key)/len(df.values))})

    expected_assists = 0

    for key in assists.keys():
        expected_assists += (key * assists.get(key))

    return expected_assists


def calculate_steals(df):

    steals = {}

    for game in df.values:

        if (game[9] in steals.keys()):
            steals.update({game[9]: (steals.get(game[9]) + 1)})
        else:
            steals.update({game[9]: 1})

    steals = collections.OrderedDict(sorted(steals.items()))

    for key in steals.keys():
        steals.update({key: (steals.get(key)/len(df.values))})

    expected_steals = 0

    for key in steals.keys():
        expected_steals += (key * steals.get(key))

    return expected_steals


def calculate_blocks(df):

    blocks = {}

    for game in df.values:

        if (game[10] in blocks.keys()):
            blocks.update({game[10]: (blocks.get(game[10]) + 1)})
        else:
            blocks.update({game[10]: 1})

    blocks = collections.OrderedDict(sorted(blocks.items()))

    for key in blocks.keys():
        blocks.update({key: (blocks.get(key)/len(df.values))})

    expected_blocks = 0

    for key in blocks.keys():
        expected_blocks += (key * blocks.get(key))

    return expected_blocks


def calculate_turnovers(df):

    turnovers = {}

    for game in df.values:

        if (game[8] in turnovers.keys()):
            turnovers.update({game[8]: (turnovers.get(game[8]) + 1)})
        else:
            turnovers.update({game[8]: 1})

    turnovers = collections.OrderedDict(sorted(turnovers.items()))

    for key in turnovers.keys():
        turnovers.update({key: (turnovers.get(key)/len(df.values))})

    expected_turnovers = 0

    for key in turnovers.keys():
        expected_turnovers += (key * turnovers.get(key))

    return expected_turnovers


def calculate_minutes(df, team_id):

    minutes = {}

    global player_id

    for game in df.values:

        player_id = game[1]

        if (game[4] in minutes.keys()):
            minutes.update({game[4]: (minutes.get(game[4]) + 1)})
        else:
            minutes.update({game[4]: 1})

    minutes = collections.OrderedDict(sorted(minutes.items()))

    team_logs = teamgamelogs.TeamGameLogs(
        team_id_nullable=team_id, season_nullable="2020-21", season_type_nullable="Playoffs", last_n_games_nullable=10).get_data_frames()

    num_games = len(team_logs[0].values)

    for key in minutes.keys():
        minutes.update({key: (minutes.get(key)/num_games)})

    expected_minutes = 0

    for key in minutes.keys():
        expected_minutes += (key * minutes.get(key))

    return expected_minutes
