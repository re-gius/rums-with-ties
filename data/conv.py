import argparse
import csv
from collections import defaultdict

def save_file(fout, header, data):
    with open(fout, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

def parse_oreo(fin):
    lines = []
    items = []
    reviews = []
    num_users = 6
    with open (fin, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvreader:
            if 'oreo' not in row[0]:
                items.append(row[0])
                reviews.append(row[1:1+num_users])
    name_dataset = "oreo"
    num_items = len(items)
    for i in range(num_users):
        line_i = []
        for j in range(num_items):
            line_i.append(reviews[j][i])
        lines.append(line_i)
    return name_dataset, num_users, num_items, items, lines

def parse_trip(fin):
    lines = []
    items = []
    num_items = 10
    with open (fin, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvreader:
            if 'ID' not in row[0]:
                lines.append(row[1:])
            else:
                items = row[1:]
    name_dataset = "tripadvisor"
    num_users = len(lines)
    return name_dataset, num_users, num_items, items, lines

def parse_sushi(fin, top_n):
    lines = []
    num_items = 100
    preferences_count = [0]*100
    """
    with open(fitems) as f:
        for l in f:
            line = l.split(':')
            items.append(line[1][:-1])
    """
    with open (fin, newline='') as f:
        for l in f:
            l_split = l.split()
            preferences = [i for i in range(num_items) if l_split[i][0]!='-']
            for i in preferences:
                preferences_count[i]+=1
    sorted_items = sorted(range(len(preferences_count)), key=lambda k: -preferences_count[k])
    top_n_items = [i for i in range(num_items) if sorted_items[i] < top_n]
    with open (fin, newline='') as f:
        for l in f:
            preferences = [x[0] for x in l.split()]
            filtered_preferences = [preferences[i] for i in top_n_items]
            slate = [x for x in filtered_preferences if x!='-']
            if len(slate) > 1:
                lines.append(filtered_preferences)
    name_dataset = "sushi"
    num_users = len(lines)
    top_n_items = [str(i) for i in top_n_items]
    return name_dataset, num_users, top_n, top_n_items, lines

def parse_moviebook(fin, top_n, name_dataset):
    lines = []
    preferences_count = defaultdict(int)
    with open (fin, newline='') as f:
        csvreader = csv.reader(f, delimiter=',', quotechar='|')
        for l in csvreader:
            if 'user' not in l[0]:
                preferences_count[l[1]]+=1
    sorted_items = [k for k, _ in sorted(preferences_count.items(), key=lambda item: -item[1])]
    top_n_items = sorted_items[:top_n]
    top_items_dict = {top_n_items[i]:i for i in range(top_n)}
    users2slates = {}
    with open (fin, newline='') as f:
        csvreader = csv.reader(f, delimiter=',', quotechar='|')
        next(csvreader)
        for l in csvreader:
            user = int(l[0])
            movie = l[1]
            if user not in users2slates:
                users2slates[user] = ['-']*top_n
            if movie in top_n_items:
                users2slates[user][top_items_dict[movie]] = l[2]
    for _, pref in users2slates.items():
        slate = [x for x in pref if x!='-']
        if len(slate) > 1:
            lines.append(pref)
    num_users = len(lines)
    return name_dataset, num_users, top_n, top_n_items, lines

def parse_young(fin):
    lines = []
    items = []
    num_items = 7
    with open (fin, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvreader:
            if 'music' not in row[0].lower():
                lines.append(row[133:133+num_items])
            else:
                items = row[138:138+num_items]
                items = [item[1:-1] for item in items]
    name_dataset = "young_people_spending_habits"
    num_users = len(lines)
    return name_dataset, num_users, num_items, items, lines

parser = argparse.ArgumentParser()
parser.add_argument("f", nargs="+")
parser.add_argument("--basedir", default="./clean/")
parser.add_argument("--seed", type=int, default=42)
parser.add_argument("--maxn_sushi", type=int, default=10)
parser.add_argument("--maxn_movies", type=int, default=20)
parser.add_argument("--maxn_books", type=int, default=30)

args = parser.parse_args()

for f in args.f:
    print(f)
    if "oreo" in f.lower():
        o = parse_oreo(f)
    elif "tripadvisor" in f.lower():
        o = parse_trip(f)
    elif "sushi" in f.lower():
        o = parse_sushi(f, args.maxn_sushi)
    elif "movie" in f.lower():
        o = parse_moviebook(f, args.maxn_movies, "movies")
    elif "young" in f.lower():
        o = parse_young(f)
    elif "book" in f.lower():
        o = parse_moviebook(f, args.maxn_books, "books")
    else:
        print("Unkown format:", f)
        continue
    name_dataset, num_users, num_items, items, lines = o
    fout = f"{args.basedir}/{name_dataset}_{num_items}_{num_users}.csv"
    print(f'{name_dataset} num_items={num_items}, num_users={num_users}')
    save_file(fout, items, lines)
