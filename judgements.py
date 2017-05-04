"""
Created by Jimmy (April 2017)
Load and validate judgment data which could include understandability, readability or other judgement files
"""

import os


def load_judgements(judgements_path, judgements):
    if not os.path.exists(judgements_path):
        raise NameError("Path to judgement file not found!")

    with open(judgements_path, 'r') as infile:
        for line in infile:
            parts = line.split()
            key = parts[0] + "*" + parts[2]

            try:
                judgements[key] *= (float(parts[3])/100)
            except KeyError:
                judgements[key] = (float(parts[3])/100)
