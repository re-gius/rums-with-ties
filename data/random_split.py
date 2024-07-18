import argparse, random
import csv, random

def save_file(fout, header, data):
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

# Does a random split of lines into train/test with train_frac proportion
def random_split(lines, train_frac):
    random.shuffle(lines)
    train_size = int(train_frac*len(lines))
    training_set = lines[:train_size]
    test_set = lines[train_size:]
    return training_set, test_set


parser = argparse.ArgumentParser()
parser.add_argument("f", nargs="+")
parser.add_argument("--basedir", default="./clean")
parser.add_argument("--seed", type=int, default=42)
parser.add_argument("--trainfrac", type=float, default=0.8)

args = parser.parse_args()

for f in args.f:
    print(f)
    name_file, num_users, num_items, items, lines = parse_clean(f)
    random.seed(args.seed)
    if "csv" in f:
        training_set, test_set = random_split(lines, args.trainfrac)
    else:
        print("Unkown format:", f)
        continue
    fout = f"{args.basedir}/train/{name_file}_train.csv"
    print(fout)
    save_file(fout, items, training_set)
    fout = f"{args.basedir}/test/{name_file}_test.csv"
    print(fout)
    save_file(fout, items, test_set)
