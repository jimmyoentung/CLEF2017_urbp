"""
Created by Jimmy (April 2017)
Implementation of Rank-Biased Precision based on: "Rank-Biased Precision for Measurement of Retrieval Effectiveness",
Moffat, A. and Zobel, J., ACM Transactions on Information Systems, Vol. 27, No. 1, Article 2, December 2008.
"""

import run
import judgements
import persist
import urbp
import qrel
import time
import argparse

# read parameters
parser = argparse.ArgumentParser()

parser.add_argument("files", help="USAGE: [options] <qrels-file> <run-file> <judgement file 1, e.g.,qrels-file> .. "
                                  "<judgement file n, e.g.,understandability-file>",
                    action="store", nargs="*")

parser.add_argument("-d",
                    "--depth",
                    help="ranking depths to calculate rbp to. A positive integer or 0 to indicate to calculate for "
                         "all documents in the run.",
                    type=int)

parser.add_argument("-p",
                    "--persist",
                    help="user persistences to calculate rbp with.  A comma-separated list of floats "
                         "in range [0.0,1.0]")

parser.add_argument("-q",
                    "--print_detail",
                    action='store_true',
                    help="print rbp values for each query (default is only give the overall averages)")

parser.add_argument("-T",
                    "--no_overall",
                    action='store_true',
                    help="do not print overall averages ('T'otals)")

parser.add_argument("-b",
                    "--relevance_threshold",
                    help="convert relevance judgments in qrels file to binary at the given threshold (default 1)",
                    type=int)


args = parser.parse_args()


# parse depth parameter
if args.depth:
    depth = args.depth
else:
    depth = 0

# parse depth parameter
if args.persist:
    persists_string = args.persist
else:
    persists_string = ""

# parse q / print detail parameter
if args.print_detail:
    print_detail = True
else:
    print_detail = False

# parse T/ print overall parameter
if args.no_overall:
    print_overall = False
else:
    print_overall = True

# parse relevance threshold
if args.relevance_threshold:
    relevance_threshold = args.relevance_threshold
else:
    relevance_threshold = 1

# parse files: run, qrels and judgements files
# initialise judgements files which could be understandability, readability or other judgement files
judgements_score = dict()

if len(args.files) >= 2:
    qrels_path = args.files[0]
    runs_path = args.files[1]

    qrels = qrel.load_qrels(qrels_path, relevance_threshold)

    for i in range(2, len(args.files), 1):
        judgements.load_judgements(args.files[i], judgements_score)
else:
    raise NameError("Missing required parameter(s): path to run file and at least 1 (one) judgement file, e.g., qrels, "
                    "understandability!")


# Check if the params are not printing detail and overall then there will be no output. so raise error
if not print_detail and not print_overall:
    raise NameError("Given parameters are not printing detail and overall thus there will be no output!")

startTime = time.time()

# load runs and persists into the respected list
runs, query_ids = run.load_runs(runs_path)
persists = persist.load_persist(persists_string)

rbps, all_rbps = urbp.compute_urbp(query_ids, runs, qrels, persists, depth, judgements_score)

if print_detail:
    for rbp in rbps:
        print("p= {0:.2f} q= {1} d= {2} rbp= {3:.4f} + {4:.4f}".format(rbp.persist, rbp.q, rbp.d, rbp.score, rbp.err))

if print_overall:
    for rbp in all_rbps:
        print("p= {0:.2f} q= {1} d= {2} rbp= {3:.4f} + {4:.4f}".format(rbp.persist, rbp.q, rbp.d, rbp.score, rbp.err))


print("Duration ", time.time()-startTime)
