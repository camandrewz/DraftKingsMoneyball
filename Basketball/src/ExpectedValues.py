import collections
import statistics
from nba_api.stats.endpoints import teamgamelogs

LOOKBACK = 10

def calculate_threes(player, df):

    fgm = {}
    fgm_list = []

    if player.injury_status:
        lookback_num = len(df.values)
    else:
        lookback_num = LOOKBACK

    for game in df.values:

        fgm_list.append(game[5])

        if (game[5] in fgm):
            fgm[game[5]] = fgm[game[5]] + 1
        else:
            fgm[game[5]] = 1

    fgm = collections.OrderedDict(sorted(fgm.items()))

    for key in fgm:
        fgm[key] = (fgm[key]/lookback_num)

    expected_value = 0

    for key in fgm:
        expected_value += (key * fgm[key])

    while len(fgm_list) < lookback_num:
        fgm_list.append(0)

    player.set_expected_threes(expected_value)
    player.set_average_threes(statistics.mean(fgm_list))
    player.set_std_deviation_threes(statistics.stdev(fgm_list))


def calculate_pts(player, df):

    pts = {}
    pts_list = []

    if player.injury_status:
        lookback_num = len(df.values)
    else:
        lookback_num = LOOKBACK

    for game in df.values:

        pts_list.append(game[11])

        if (game[11] in pts):
            pts[game[11]] = pts[game[11]] + 1
        else:
            pts[game[11]] = 1

    pts = collections.OrderedDict(sorted(pts.items()))

    for key in pts:
        pts[key] = pts[key]/lookback_num

    expected_pts = 0

    for key in pts:
        expected_pts += (key * pts[key])

    while len(pts_list) < lookback_num:
        pts_list.append(0)

    player.set_expected_pts(expected_pts)
    player.set_average_pts(statistics.mean(pts_list))
    player.set_std_deviation_pts(statistics.stdev(pts_list))


def calculate_rebounds(player, df):

    rebounds = {}
    rebounds_list = []

    if player.injury_status:
        lookback_num = len(df.values)
    else:
        lookback_num = LOOKBACK

    for game in df.values:

        rebounds_list.append(game[6])

        if (game[6] in rebounds):
            rebounds[game[6]] = rebounds[game[6]] + 1
        else:
            rebounds[game[6]] = 1

    rebounds = collections.OrderedDict(sorted(rebounds.items()))

    for key in rebounds:
        rebounds[key] = (rebounds[key]/lookback_num)

    expected_rebounds = 0

    for key in rebounds:
        expected_rebounds += (key * rebounds[key])

    while len(rebounds_list) < lookback_num:
        rebounds_list.append(0)

    player.set_expected_rebounds(expected_rebounds)
    player.set_average_rebounds(statistics.mean(rebounds_list))
    player.set_std_deviation_rebounds(statistics.stdev(rebounds_list))


def calculate_assists(player, df):

    assists = {}
    assists_list = []

    if player.injury_status:
        lookback_num = len(df.values)
    else:
        lookback_num = LOOKBACK

    for game in df.values:

        assists_list.append(game[7])

        if (game[7] in assists):
            assists[game[7]] = assists[game[7]] + 1
        else:
            assists[game[7]] = 1

    assists = collections.OrderedDict(sorted(assists.items()))

    for key in assists:
        assists[key] = assists[key]/lookback_num

    expected_assists = 0

    for key in assists:
        expected_assists += (key * assists[key])

    while len(assists_list) < lookback_num:
        assists_list.append(0)

    player.set_expected_assists(expected_assists)
    player.set_average_assists(statistics.mean(assists_list))
    player.set_std_deviation_assists(statistics.stdev(assists_list))


def calculate_steals(player, df):

    steals = {}
    steals_list = []

    if player.injury_status:
        lookback_num = len(df.values)
    else:
        lookback_num = LOOKBACK

    for game in df.values:

        steals_list.append(game[9])

        if (game[9] in steals):
            steals[game[9]] = steals[game[9]] + 1
        else:
            steals[game[9]] = 1

    steals = collections.OrderedDict(sorted(steals.items()))

    for key in steals:
        steals[key] = steals[key]/lookback_num

    expected_steals = 0

    for key in steals:
        expected_steals += (key * steals[key])

    while len(steals_list) < lookback_num:
        steals_list.append(0)

    player.set_expected_steals(expected_steals)
    player.set_average_steals(statistics.mean(steals_list))
    player.set_std_deviation_steals(statistics.stdev(steals_list))


def calculate_blocks(player, df):

    blocks = {}
    blocks_list = []

    if player.injury_status:
        lookback_num = len(df.values)
    else:
        lookback_num = LOOKBACK

    for game in df.values:

        blocks_list.append(game[10])

        if (game[10] in blocks):
            blocks[game[10]] = blocks[game[10]] + 1
        else:
            blocks[game[10]] = 1

    blocks = collections.OrderedDict(sorted(blocks.items()))

    for key in blocks:
        blocks[key] = blocks[key]/lookback_num

    expected_blocks = 0

    for key in blocks:
        expected_blocks += (key * blocks[key])

    while len(blocks_list) < lookback_num:
        blocks_list.append(0)

    player.set_expected_blocks(expected_blocks)
    player.set_average_blocks(statistics.mean(blocks_list))
    player.set_std_deviation_blocks(statistics.stdev(blocks_list))


def calculate_turnovers(player, df):

    turnovers = {}
    turnovers_list = []

    if player.injury_status:
        lookback_num = len(df.values)
    else:
        lookback_num = LOOKBACK

    for game in df.values:

        turnovers_list.append(game[8])

        if (game[8] in turnovers):
            turnovers[game[8]] = turnovers[game[8]] + 1
        else:
            turnovers[game[8]] = 1

    turnovers = collections.OrderedDict(sorted(turnovers.items()))

    for key in turnovers:
        turnovers[key] = turnovers[key]/lookback_num

    expected_turnovers = 0

    for key in turnovers:
        expected_turnovers += (key * turnovers[key])

    while len(turnovers_list) < lookback_num:
        turnovers_list.append(0)

    player.set_expected_turnovers(expected_turnovers)
    player.set_average_turnovers(statistics.mean(turnovers_list))
    player.set_std_deviation_turnovers(statistics.stdev(turnovers_list))


def calculate_minutes(player, df, team_id):

    minutes = {}

    global player_id

    for game in df.values:

        player_id = game[1]

        if (game[4] in minutes):
            minutes[game[4]] = minutes[game[4]] + 1
        else:
            minutes[game[4]] = 1

    minutes = collections.OrderedDict(sorted(minutes.items()))

    team_logs = teamgamelogs.TeamGameLogs(
        team_id_nullable=team_id, season_nullable="2020-21", season_type_nullable="Playoffs", last_n_games_nullable=LOOKBACK).get_data_frames()

    num_games = len(team_logs[0].values)

    for key in minutes:
        minutes[key] = minutes[key]/num_games

    expected_minutes = 0

    for key in minutes:
        expected_minutes += (key * minutes[key])

    player.set_expected_minutes(expected_minutes)
