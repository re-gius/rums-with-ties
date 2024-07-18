import argparse
import csv

def save_mnl_file(fout, header, data):
    with open(fout, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

def parse_slates(fin):
    lines = []
    items = []
    file_path = fin.split('/')
    name_file = file_path[-1][:-4]
    with open (fin, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        items = next(csvreader)
        for row in csvreader:
            lines.append(row)
    return name_file, items, lines

def get_slate_winner(preferences, delta):    
    max_elem = max(preferences)
    if sum(map(lambda x : x!='-' and x!='' and float(x) >= float(max_elem) - delta, preferences)) > 1:
        return -1
    return preferences.index(max_elem)

def get_onehot_format(slates, items, delta):
    wide_table = []
    new_items = ['slate_ID'] + items + ['no-choice'] + ['CHOICE']
    i = 1
    for slate in slates:
        modified_slate = [i] + list(map(lambda x : int(x!='-' and x!=''), slate))
        winner_index = get_slate_winner(slate, delta)
        modified_slate.append(1)
        if winner_index == -1:
            winner_index = len(slate)
        modified_slate.append(winner_index+1)
        wide_table.append(modified_slate)
        i+=1
    return new_items, wide_table


parser = argparse.ArgumentParser()
parser.add_argument("f", nargs="+")
parser.add_argument("--basedir", default="./mnl_datasets")
parser.add_argument("--delta", type=float, default=0.5)

args = parser.parse_args()

for f in args.f:
    print(f)
    name_file, items, slates = parse_slates(f)
    if "oreo" in f or "sushi" in f or "movie" in f or "book" in f or "tripadvisor" in f or "young" in f:
        new_items, wide_slates_table = get_onehot_format(slates, items, args.delta)
    else:
        print("Unkown dataset:", f)
        continue
    if "train" in name_file:
        fout = f"{args.basedir}/train/{name_file[:-6]}_{args.delta}_train.csv"
    elif "test" in name_file:
        fout = f"{args.basedir}/test/{name_file[:-5]}_{args.delta}_test.csv"
    else:
        if "train" in f:
            fout = f"{args.basedir}/train/{name_file}_{args.delta}.csv"
        elif "test" in f:
            fout = f"{args.basedir}/test/{name_file}_{args.delta}.csv"
        else:
            fout = f"{args.basedir}/{name_file}_{args.delta}.csv"
    print(fout)
    save_mnl_file(fout, new_items, wide_slates_table)
