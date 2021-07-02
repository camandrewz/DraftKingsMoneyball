from src import Lineup
import hashlib
import bisect

top_n_lineups = []
top_n_lineups_showdown = []

n = 250

'''

for i in range(0, n):
    top_n_lineups_showdown.append({"CAPTAIN": {}, "UTIL1": {}, "UTIL2": {}, "UTIL3": {},
                                   "UTIL4": {}, "UTIL5": {}, "PRJ": 0, "PRJ*MIN": 0, "COST": 0})

    top_n_lineups.append({"PG": {}, "SG": {}, "SF": {}, "PF": {}, "C": {}, "GUARD": {},
                          "FORWARD": {}, "UTIL": {}, "PRJ": 0, "PRJ*MIN": 0, "COST": 0})

'''


def add_to_top_lineups(lineup, showdown):

    if showdown:
        bisect.insort(top_n_lineups_showdown, lineup)
        if len(top_n_lineups_showdown) > n:
            del top_n_lineups_showdown[n]

    '''

        for index, element in enumerate(top_n_lineups_showdown):
            if (lineup.projection > element.projection):
                top_n_lineups_showdown.insert(index, lineup)
                del top_n_lineups_showdown[n]
                return

    else:
        for index, element in enumerate(top_n_lineups):

            if (lineup_score > element.get("PRJ")):
                top_n_lineups.insert(index, lineup)
                del top_n_lineups[n]
                return

    '''


def create_signature(captain, util1, util2, util3, util4, util5):

    names = [captain, util1, util2, util3, util4, util5]
    names.sort()

    unencoded_str = names[0] + names[1] + names[2] + names[3] + names[4]

    encodedStr = hashlib.md5(unencoded_str.encode()).hexdigest()

    return encodedStr


def create_best_lineups(final_dataFrame, point_guards, shooting_guards, small_forwards, power_forwards, centers, all_guards, all_forwards):

    print("Creating Lineups...")

    current_iteration = 1

    for pg in point_guards.values:

        for sg in shooting_guards.values:

            if (sg[0] == pg[0]):
                continue

            for sf in small_forwards.values:

                if (sf[0] == sg[0] or sf[0] == pg[0]):
                    continue

                for pf in power_forwards.values:

                    if (pf[0] == sf[0] or pf[0] == sg[0] or pf[0] == pg[0]):
                        continue

                    for center in centers.values:

                        if (center[0] == pf[0] or center[0] == sf[0] or center[0] == sg[0] or center[0] == pg[0]):
                            continue

                        for guard in all_guards.values:

                            if (guard[0] == sg[0] or guard[0] == pg[0]):
                                continue

                            for forward in all_forwards.values:

                                if (forward[0] == pf[0] or forward[0] == sf[0] or forward[0] == center[0]):
                                    continue

                                for util in final_dataFrame.values:

                                    if (util[0] == pg[0] or util[0] == sg[0] or util[0] == sf[0] or util[0] == pf[0] or util[0] == center[0] or util[0] == guard[0] or util[0] == forward[0]):
                                        continue

                                    if (pg[11] + sg[11] + sf[11] + pf[11] + center[11] + guard[11] + forward[11] + util[11]) > 50000:
                                        continue

                                    current_lineup = {"PG": {"NAME": pg[0], "PRJ": pg[12], "SALARY": pg[11]},
                                                      "SG": {"NAME": sg[0], "PRJ": sg[12], "SALARY": sg[11]},
                                                      "SF": {"NAME": sf[0], "PRJ": sf[12], "SALARY": sf[11]},
                                                      "PF": {"NAME": pf[0], "PRJ": pf[12], "SALARY": pf[11]},
                                                      "C": {"NAME": center[0], "PRJ": center[12], "SALARY": center[11]},
                                                      "GUARD": {"NAME": guard[0], "PRJ": guard[12], "SALARY": guard[11]},
                                                      "FORWARD": {"NAME": forward[0], "PRJ": forward[12], "SALARY": forward[11]},
                                                      "UTIL": {"NAME": util[0], "PRJ": util[12], "SALARY": util[11]},
                                                      "PRJ": 0, "PRJ*MIN": 0, "COST": 0}

                                    current_lineup["COST"] = pg[11] + sg[11] + sf[11] + \
                                        pf[11] + center[11] + \
                                        guard[11] + forward[11] + util[11]

                                    current_lineup["PRJ*MIN"] = pg[13] + sg[13] + sf[13] + \
                                        pf[13] + center[13] + guard[13] + \
                                        forward[13] + util[13]

                                    current_lineup["PRJ"] = pg[12] + sg[12] + sf[12] + \
                                        pf[12] + center[12] + \
                                        guard[12] + forward[12] + util[12]

                                    add_to_top_lineups(
                                        current_lineup, current_lineup.get("PRJ"), False)

                                    current_iteration += 1

                                    if (current_iteration % 1000000 == 0):
                                        print(
                                            "Current Iteration: " + str(int(current_iteration/1000000)) + ",000,000")

    print("Total Lineups Checked: ", current_iteration)
    return top_n_lineups


def create_best_lineups_showdown(all_players):

    print("\n")
    print("Creating Lineups...")

    signatures = {}

    current_iteration = 1

    for captain in all_players:

        for util1 in all_players:

            if (util1.name == captain.name):
                continue

            for util2 in all_players:

                if (util2.name == util1.name or util2.name == captain.name):
                    continue

                for util3 in all_players:

                    if (util3.name == util1.name or util3.name == util2.name or util3.name == captain.name):
                        continue

                    for util4 in all_players:

                        if (util4.name == util1.name or util4.name == util2.name or util4.name == util3.name or util4.name == captain.name):
                            continue

                        for util5 in all_players:

                            if (util5.name == util1.name or util5.name == util2.name or util5.name == util3.name or util5.name == util4.name or util5.name == captain.name):
                                continue

                            sig = create_signature(
                                captain.name, util1.name, util2.name, util3.name, util4.name, util5.name)

                            if(sig in signatures):
                                continue
                            else:

                                signatures[sig] = True

                            if ((captain.salary * 1.5) + util1.salary + util2.salary + util3.salary + util4.salary + util5.salary) > 50000:
                                continue

                            current_iteration += 1

                            if (current_iteration % 10000 == 0):
                                print(
                                    "Current Lineup #: " + str(current_iteration))

                            '''

                            current_lineup = {"CAPTAIN": {"NAME": captain[0], "PRJ": (captain[12] * 1.5), "SALARY": (captain.salary * 1.5)},
                                              "UTIL1": {"NAME": util1[0], "PRJ": util1[12], "SALARY": util1.salary},
                                              "UTIL2": {"NAME": util2[0], "PRJ": util2[12], "SALARY": util2.salary},
                                              "UTIL3": {"NAME": util3[0], "PRJ": util3[12], "SALARY": util3.salary},
                                              "UTIL4": {"NAME": util4[0], "PRJ": util4[12], "SALARY": util4.salary},
                                              "UTIL5": {"NAME": util5[0], "PRJ": util5[12], "SALARY": util5.salary},
                                              "PRJ": 0, "PRJ*MIN": 0, "COST": 0}

                            '''

                            current_lineup = Lineup.Lineup(
                                captain, util1, util2, util3, util4, util5, sig)
                            current_lineup.set_total_cost()
                            current_lineup.set_projection()

                            '''

                            current_lineup["PRJ*MIN"] = (
                                captain[13] * 1.5) + util1[13] + util2[13] + util3[13] + util4[13] + util5[13]

                            '''

                            add_to_top_lineups(current_lineup, True)

    print("Total Valid Lineups Checked: ", current_iteration)
    return top_n_lineups_showdown


def monte_carlo_simulations(top_lineups, num_simulations):

    total_wins = {}

    for lineup in top_lineups:
        total_wins.update({lineup.signature: {"WINS":0, "LOSSES":0, "TIES":0}})

    for simulation in range(0, num_simulations):

        previous_matches = {}

        for lineup in top_lineups:
            lineup.set_random_projection()

        for lineup in top_lineups:
            for lineup2 in top_lineups:

                if lineup.signature == lineup2.signature:
                    continue

                combined_hash = [lineup.signature, lineup2.signature]
                combined_hash.sort()
                combined_hash_str = combined_hash[0] + combined_hash[1]

                if combined_hash_str in previous_matches:
                    continue
                else:
                    previous_matches.update({combined_hash_str: True})

                if lineup.random_projection > lineup2.random_projection:
                    total_wins[lineup.signature]["WINS"] = total_wins[lineup.signature]["WINS"] + 1
                    total_wins[lineup2.signature]["LOSSES"] = total_wins[lineup2.signature]["LOSSES"] + 1
                elif lineup2.random_projection > lineup.random_projection:
                    total_wins[lineup2.signature]["WINS"] = total_wins[lineup2.signature]["WINS"] + 1
                    total_wins[lineup.signature]["LOSSES"] = total_wins[lineup.signature]["LOSSES"] + 1
                elif lineup.random_projection == lineup2.random_projection:
                    total_wins[lineup2.signature]["TIES"] = total_wins[lineup2.signature]["TIES"] + 1
                    total_wins[lineup.signature]["TIES"] = total_wins[lineup.signature]["TIES"] + 1

    return total_wins
