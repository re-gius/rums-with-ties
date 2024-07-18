import argparse, random
from email.policy import default
import itertools
import csv, random
from collections import defaultdict

def save_lp_sol_parsed(fout, bucket_values_dict):
    with open(fout, "w", newline='') as f:
        writer = csv.writer(f)
        for bucket, value in bucket_values_dict.items():
            writer.writerow([str(value),str(bucket)])

def parse_lp_sol(fin):
    name_file = fin.split('/')[-1][:-3]
    bucket_values_dict = defaultdict(float)
    with open (fin, "r") as f:
        for l in f.readlines():
            if "variable name=\"prob_" in l and "value=\"0\"" not in l:
                l_split = l.split()
                bucket = ((l_split[1]).split('_'))[1][:-1]
                value = float((l_split[4]).split("\"")[1])
                bucket_values_dict[bucket] = value
    return name_file, bucket_values_dict


parser = argparse.ArgumentParser()
parser.add_argument("f", nargs="+")
parser.add_argument("--basedir", default="./lp_rumwt")

args = parser.parse_args()

for f in args.f:
    print(f)
    name_file, bucket_values_dict = parse_lp_sol(f)
    fout = f"{args.basedir}/{name_file}_learned_rumwt.csv"
    save_lp_sol_parsed(fout, bucket_values_dict)
    