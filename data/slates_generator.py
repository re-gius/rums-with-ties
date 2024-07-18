import argparse, random
import csv, random
from itertools import combinations
from collections import defaultdict

def save_slate_file(fout, header, data):
    with open(fout, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

def parse_clean(fin):
    lines = []
    items = []
    file_path = fin.split('/')
    name_file = file_path[-1][:-4]
    with open (fin, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        items = next(csvreader)
        for row in csvreader:
            lines.append(row)
    num_items = len(items)
    num_users = len(lines)
    return name_file, num_users, num_items, items, lines

# samples num_slates slates UAR among the slates with size slate_size in [n]
def sample_slates(n, slate_size, num_slates):
    slates = []
    items = range(n)
    for _ in range(num_slates):
        slate = random.sample(items, slate_size)
        slate.sort()
        slates.append(slate)
    return slates

# samples num_slates slates UAR among the given feasible_slates
def sample_slates_constr(lines, feasible_slates_dict, num_slates):
    sampled_slates = []
    feasible_slates_items = list(feasible_slates_dict.items())
    for _ in range(num_slates):
        slate_enc, indices = random.choice(feasible_slates_items)
        slate = [int(x) for x in slate_enc.split('.')]
        i = random.choice(indices)
        expl_slate = ['-']*len(lines[0])
        for j in slate:
            expl_slate[j] = lines[i][j]
        sampled_slates.append(expl_slate)
    return sampled_slates

# Returns all the slate with given size and frequency>=min_freq in lines
def feasible_slates(lines, slate_size, min_freq):
    slates_dict = defaultdict(list)
    n = len(lines[0])
    for ind in range(len(lines)):
        l = lines[ind]
        slate = [i for i in range(n) if l[i]!='-']
        if len(slate) >= slate_size:
            for subslate in combinations(slate, slate_size):
                subslate_enc = '.'.join(str(x) for x in subslate)
                slates_dict[subslate_enc].append(ind)
    return {k:v for (k,v) in slates_dict.items() if len(v) >= min_freq}

# Returns all the slates of [n] with a given size slate_size
def all_kslates(n, slate_size):
    universe = range(n)
    slates = []
    for slate in combinations(universe, slate_size):
        slates.append(list(slate))
    return slates

def explicit_slates(lines, slates_indices):
    expl_slates = []
    num_users = len(lines)
    for slate_i in slates_indices:
        expl_slate = ['-']*len(lines[0])
        i = random.randint(0, num_users-1)
        for j in slate_i:
            expl_slate[j] = lines[i][j]
        expl_slates.append(expl_slate)
    return expl_slates


parser = argparse.ArgumentParser()
parser.add_argument("f", nargs="+")
parser.add_argument("--basedir", default="./slates")
parser.add_argument("--seed", type=int, default=42)
parser.add_argument("--slatesize", type=int, default=3)
parser.add_argument("--numslates", type=int, default=1000)
parser.add_argument("--minfreq", type=int, default=3)

args = parser.parse_args()

for f in args.f:
    print(f)
    name_file, num_users, num_items, items, lines = parse_clean(f)
    name_file = name_file[:-6]
    random.seed(args.seed)
    if "oreo" in f or "sushi" in f or "movie" in f or "book" in f:
        slates_dict = feasible_slates(lines, args.slatesize, args.minfreq)
        print(len(slates_dict))
        sampled_slates = sample_slates_constr(lines, slates_dict, args.numslates)
    elif "tripadvisor" in f or "young" in f:
        slates_indices = sample_slates(num_items, args.slatesize, args.numslates)
        sampled_slates = explicit_slates(lines, slates_indices)
    else:
        print("Unkown format:", f)
        continue
    if "train" in f:
        fout = f"{args.basedir}/train/{name_file}_{args.slatesize}_{args.numslates}_train.csv"
        print(fout)
        save_slate_file(fout, items, sampled_slates)
    elif "test" in f:
        fout = f"{args.basedir}/test/{name_file}_{args.slatesize}_{args.numslates}_test.csv"
        print(fout)
        save_slate_file(fout, items, sampled_slates)
    else:
        fout = f"{args.basedir}/{name_file}_{args.slatesize}_{args.numslates}.csv"
        print(fout)
        save_slate_file(fout, items, sampled_slates)
