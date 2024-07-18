import argparse, random
import csv, random
from itertools import combinations
from collections import defaultdict

def save_winner_probs_file(fout, data):
    with open(fout, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def save_winners_file(fout, data):
    with open(fout, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows([[d] for d in data])

def parse_csv(fin, skip_first=True):
    lines = []
    with open (fin, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        if skip_first:
            next(csvreader)
        for row in csvreader:
            lines.append(row)
    return lines

def parse_slates(fin):
    lines = []
    file_path = fin.split('/')
    name_file = file_path[-1][:-4]
    name_file_split = name_file.split('_')
    if "train" in name_file or "test" in name_file:
        name_file = '_'.join(name_file_split[:-1])
        slate_size = int(name_file_split[-4])
    else:
        slate_size = int(name_file_split[-3])
    with open (fin, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(csvreader)
        for row in csvreader:
            lines.append(row[1:-2])
    return name_file, slate_size, lines

def get_slate_winner(preferences, delta):    
    max_elem = max(preferences)
    if sum(map(lambda x : x!='-' and float(x) >= float(max_elem) - delta, preferences)) > 1:
        return -1
    return preferences.index(max_elem)

def mle_winners(winner_probs):
    return [1+w_p.index(max(w_p)) for w_p in winner_probs]

def buckets_2_slatesdistr(lines_test, slates):
    winner_probs = []
    bucket_values_dict = defaultdict(float)
    num_buckets = 2
    for l in lines_test:
        bucket_values_dict[l[1]] = float(l[0])
        max_bkt = max(1+int(x) for x in l[1])
        if max_bkt > num_buckets:
            num_buckets = max_bkt
    print(num_buckets)
    for slate in slates:
        num_items = len(slate)
        winner_prob = [0]*(num_items+1)
        enc_slate = ''.join(str(s) for s in slate)
        for bucket, value in bucket_values_dict.items():
            outcome = [str(int(enc_slate[i])*int(bucket[i])) for i in range(num_items)]
            max_elem = max(o for o in outcome)
            max_counts = outcome.count(max_elem)
            if max_counts > 1:
                winner_prob[-1] += value
            else:
                winner_prob[outcome.index(max_elem)] += value
        winner_probs.append(winner_prob)
    return winner_probs


parser = argparse.ArgumentParser()
parser.add_argument("f", nargs="+")
parser.add_argument("--basedir", default="./lp_rumwt_pred")
parser.add_argument("--lprum", default="")
parser.add_argument("--seed", type=int, default=42)

args = parser.parse_args()

for f in args.f:
    print(f)
    name_file, slate_size, slates = parse_slates(f)
    name_rum_file = 'lp_rumwt/' + args.lprum
    delta = float(name_file.split('_')[-1])
    lines_rum = parse_csv(name_rum_file, skip_first = False)
    random.seed(args.seed)
    print(name_rum_file)
    rum_winner_probs = buckets_2_slatesdistr(lines_rum, slates)
    fout_rum_wp = f"{args.basedir}/{name_file}_winner_probs_rumwt.csv"
    save_winner_probs_file(fout_rum_wp, rum_winner_probs)
    rum_winners = mle_winners(rum_winner_probs)
    fout_rum_w = f"{args.basedir}/{name_file}_winners_rumwt.csv"
    print(fout_rum_w)
    save_winners_file(fout_rum_w, rum_winners)
