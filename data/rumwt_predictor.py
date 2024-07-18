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

def parse_clean(fin):
    lines = []
    with open (fin, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
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

# samples num_slates slates UAR among the slates with size slate_size in [n]
def sample_users_full(lines, slates, delta):
    winner_probs = []
    num_users = len(lines)
    users = range(num_users)
    for i in range(len(slates)):
        slate = slates[i]
        num_items = len(slate)
        winner_prob = [0]*(num_items+1)
        for index in range(num_users):           
            preferences = [float(slate[j])*float(lines[index][j]+'0') for j in range(num_items)] 
            winner = get_slate_winner(preferences, delta)
            if winner == -1:
                winner = num_items
            winner_prob[winner] += 1
        winner_prob = [x/num_users for x in winner_prob]
        winner_probs.append(winner_prob)
    return winner_probs

# samples num_slates slates UAR among the given feasible_slates
def sample_users_constr(lines, slates, slates_dict, delta):
    winner_probs = []
    for s in slates:
        num_items = len(s)
        slate = [i for i in range(num_items) if float(s[i])>0.5]
        slate_enc = '.'.join(str(x) for x in slate)
        winner_prob = [0]*(num_items+1)
        for index in slates_dict[slate_enc]:
            preferences = [float(s[i])*float(lines[index][i]+'0') for i in range(num_items)] 
            winner = get_slate_winner(preferences, delta)
            if winner == -1:
                winner = num_items
            winner_prob[winner]+=1
        if sum(winner_prob)>0:
            winner_prob = [x/len(slates_dict[slate_enc]) for x in winner_prob]
        else:
            winner_prob = [1.0/len(winner_prob) for _ in winner_prob]
        winner_probs.append(winner_prob)
    return winner_probs

def get_slate_winner(preferences, delta):    
    max_elem = max(preferences)
    if sum(map(lambda x : x!='-' and float(x) >= float(max_elem) - delta, preferences)) > 1:
        return -1
    return preferences.index(max_elem)


# Returns all the slate with given size and frequency>=min_freq in lines
def slates2users(lines, slate_size):
    slates_dict = defaultdict(list)
    n = len(lines[0])
    for ind in range(len(lines)):
        l = lines[ind]
        slate = [i for i in range(n) if l[i]!='-']
        if len(slate) >= slate_size:
            for subslate in combinations(slate, slate_size):
                subslate_enc = '.'.join(str(x) for x in subslate)
                slates_dict[subslate_enc].append(ind)
    return slates_dict

def mle_winners(winner_probs):
    return [1+w_p.index(max(w_p)) for w_p in winner_probs]

parser = argparse.ArgumentParser()
parser.add_argument("f", nargs="+")
parser.add_argument("--basedir", default="./rumwt_pred")
parser.add_argument("--trainrum", default="")
parser.add_argument("--testrum", default="")
parser.add_argument("--seed", type=int, default=42)

args = parser.parse_args()

for f in args.f:
    print(f)
    name_file, slate_size, slates = parse_slates(f)
    name_train_file = 'clean/'
    if "train" in args.trainrum:
        name_train_file += 'train/'
    name_train_file += args.trainrum
    name_test_file = 'clean/'
    if "test" in args.testrum:
        name_test_file += 'test/'
    name_test_file += args.testrum
    delta = float(name_file.split('_')[-1])
    lines_train = parse_clean(name_train_file)
    lines_test = parse_clean(name_test_file)
    random.seed(args.seed)
    print(name_file)
    if "oreo" in f or "sushi" in f or "movie" in f or "book" in f:
        slates_dict_train = slates2users(lines_train, slate_size)
        train_winner_probs = sample_users_constr(lines_train, slates, slates_dict_train, delta)
        slates_dict_test = slates2users(lines_test, slate_size)
        test_winner_probs = sample_users_constr(lines_test, slates, slates_dict_test, delta)
    elif "tripadvisor" in f or "young" in f:
        train_winner_probs = sample_users_full(lines_train, slates, delta)
        test_winner_probs = sample_users_full(lines_test, slates, delta)
    else:
        print("Unkown format:", f)
        continue
    fout_train = f"{args.basedir}/{name_file}_winner_probs_train.csv"
    print(fout_train)
    save_winner_probs_file(fout_train, train_winner_probs)
    fout_test = f"{args.basedir}/{name_file}_winner_probs_test.csv"
    print(fout_test)
    save_winner_probs_file(fout_test, test_winner_probs)
    train_winners = mle_winners(train_winner_probs)
    fout_train = f"{args.basedir}/{name_file}_winners_train.csv"
    print(fout_train)
    save_winners_file(fout_train, train_winners)
