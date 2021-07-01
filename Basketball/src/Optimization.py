import math

top_ten_lineups = [
    {"PG": {}, "SG": {}, "SF": {}, "PF": {}, "C": {}, "GUARD": {},
     "FORWARD": {}, "UTIL": {}, "PRJ": 0, "PRJ*MIN": 0, "COST": 0},
    {"PG": {}, "SG": {}, "SF": {}, "PF": {}, "C": {}, "GUARD": {},
     "FORWARD": {}, "UTIL": {}, "PRJ": 0, "PRJ*MIN": 0, "COST": 0},
    {"PG": {}, "SG": {}, "SF": {}, "PF": {}, "C": {}, "GUARD": {},
     "FORWARD": {}, "UTIL": {}, "PRJ": 0, "PRJ*MIN": 0, "COST": 0},
    {"PG": {}, "SG": {}, "SF": {}, "PF": {}, "C": {}, "GUARD": {},
     "FORWARD": {}, "UTIL": {}, "PRJ": 0, "PRJ*MIN": 0, "COST": 0},
    {"PG": {}, "SG": {}, "SF": {}, "PF": {}, "C": {}, "GUARD": {},
     "FORWARD": {}, "UTIL": {}, "PRJ": 0, "PRJ*MIN": 0, "COST": 0},
    {"PG": {}, "SG": {}, "SF": {}, "PF": {}, "C": {}, "GUARD": {},
     "FORWARD": {}, "UTIL": {}, "PRJ": 0, "PRJ*MIN": 0, "COST": 0},
    {"PG": {}, "SG": {}, "SF": {}, "PF": {}, "C": {}, "GUARD": {},
     "FORWARD": {}, "UTIL": {}, "PRJ": 0, "PRJ*MIN": 0, "COST": 0},
    {"PG": {}, "SG": {}, "SF": {}, "PF": {}, "C": {}, "GUARD": {},
     "FORWARD": {}, "UTIL": {}, "PRJ": 0, "PRJ*MIN": 0, "COST": 0},
    {"PG": {}, "SG": {}, "SF": {}, "PF": {}, "C": {}, "GUARD": {},
     "FORWARD": {}, "UTIL": {}, "PRJ": 0, "PRJ*MIN": 0, "COST": 0},
    {"PG": {}, "SG": {}, "SF": {}, "PF": {}, "C": {}, "GUARD": {},
     "FORWARD": {}, "UTIL": {}, "PRJ": 0, "PRJ*MIN": 0, "COST": 0}
]


def add_to_top_ten(lineup, lineup_score):

    for index, element in enumerate(top_ten_lineups):

        if (math.isclose(lineup.get("PRJ"), element.get("PRJ"))):
            return

        if (lineup_score > element.get("PRJ")):
            top_ten_lineups.insert(index, lineup)
            del top_ten_lineups[10]
            return


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

                                    add_to_top_ten(
                                        current_lineup, current_lineup.get("PRJ"))

                                    current_iteration += 1

                                    if (current_iteration % 1000000 == 0):
                                        print(
                                            "Current Iteration: " + str(int(current_iteration/1000000)) + ",000,000")

    print("Total Lineups Checked: ", current_iteration)
    return top_ten_lineups
