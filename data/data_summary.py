#print main statistics about the dataset
import argparse, random
import csv, random

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

# Returns all the slate with given size and frequency>=min_freq in lines
def avg_slates_size(lines):
    n = len(lines[0])
    avg_size = 0
    for ind in range(len(lines)):
        l = lines[ind]
        slate = [i for i in range(n) if l[i]!='-']
        avg_size += len(slate)
    return avg_size/len(lines)

parser = argparse.ArgumentParser()
parser.add_argument("f", nargs="+")
parser.add_argument("--seed", type=int, default=42)

args = parser.parse_args()

for f in args.f:
    print(f)
    name_file, num_users, num_items, items, lines = parse_clean(f)
    name_file = name_file[:-6]
    random.seed(args.seed)
    print(avg_slates_size(lines))
