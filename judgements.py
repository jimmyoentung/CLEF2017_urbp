"""
Created by Jimmy (April 2017)
Load and validate judgment data which could include understandability, readability or other judgement files
"""

import os


def load_judgements(judgements_path, interpretation, judgements):
    if not os.path.exists(judgements_path):
        raise NameError("Path to judgement file not found!")

    if interpretation not in ("H", "L"):
        raise NameError("Invalid interpretation value! Valid options are: H = Higher is better or L = Lower is better")

    with open(judgements_path, 'r') as infile:
        for line in infile:
            parts = line.split()
            key = parts[0] + "*" + parts[2]

            if interpretation == "H":
                judgement_value = (float(parts[3])/100)
            else:
                judgement_value = 1 - (float(parts[3]) / 100)

            try:
                judgements[key] *= judgement_value
            except KeyError:
                judgements[key] = judgement_value
