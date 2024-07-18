import argparse, random
import itertools
import csv, random
from collections import defaultdict

def save_lp_dat(fout, s_w, s_w_probs):
    with open(fout, "w") as f:
        f.write("Slates_with_Winners = { \"")
        f.write(s_w[0])
        for i in range(1, len(s_w)):
            f.write("\", \"")
            f.write(s_w[i])
        f.write(" };\n")
        slate_size = len((s_w[0].split('_')[0]).split('.'))-1
        f.write("Buckets = { \"")
        for bucket in itertools.product(range(2), repeat=slate_size):
            bkt = ''.join(str(b) for b in bucket)
            f.write(bkt)
            if '0' in bkt:
                f.write("\", \"")
        f.write(" };\n")
        f.write("\n")
        f.write("DistrSW = [ ")
        f.write("{:.4f}".format(s_w_probs[0]))
        for i in range(1, len(s_w_probs)):
            f.write(", ")
            f.write("{:.4f}".format(s_w_probs[i]))
        f.write(" ];\n")

def save_lp_mod(fout, s_w_buckets):
    with open(fout, "w") as f:
        f.write("Slates_with_Winners = ...;\n")
        f.write("Buckets = ...;\n")
        f.write("\n")
        f.write("float DistrSW[Slates_with_Winners] = ...;")
        f.write("\n")
        f.write("dvar float+ delta[Slates_with_Winners];\n")
        f.write("dvar float+ prob[Buckets];\n")
        f.write("\n")
        f.write("minimize\n")
        f.write("\tsum( sw in Slates_with_Winners )\n")
        f.write("\t\tdelta[sw];\n")
        f.write("\n")
        f.write("subject to\n")
        f.write("\tforall( sw in Slates_with_Winners)\n")
        for i in range(len(s_w_buckets)):
            s_w_b = s_w_buckets[i]
            f.write("\t\tctswleft_"+str(i)+":\n")
            f.write("\t\t\t-delta[sw] <= DistrSW[sw] - "+" - ".join("prob[\""+s_w_bb+"\"]" for s_w_bb in s_w_b)+";\n")
        f.write("\tforall( sw in Slates_with_Winners)\n")
        for i in range(len(s_w_buckets)):
            s_w_b = s_w_buckets[i]
            f.write("\t\tctswright_"+str(i)+":\n")
            f.write("\t\t\tdelta[sw] >= DistrSW[sw] - "+" - ".join("prob[\""+s_w_bb+"\"]" for s_w_bb in s_w_b)+";\n")
        f.write("\tct_sumprobs:\n")
        f.write("\t\tsum( b in Buckets )\n")
        f.write("\t\t\tprob[b] = 1;\n")
        f.write("\tforall( b in Buckets)\n")
        f.write("\t\tct_nonneg:\n")
        f.write("\t\t\tprob[b] >= 0;")

def save_lp(fout, s_w, s_w_probs, s_w_buckets, bucket_orders):
    with open(fout, "w") as f:
        f.write("Minimize\n")
        f.write(" ")
        f.write(" + ".join("delta_"+sw for sw in s_w))
        f.write("\n")
        f.write("Subject To\n")
        for i in range(len(s_w)):
            sw_i = s_w[i]
            swb_i = s_w_buckets[i]
            f.write(" ctswleft_"+str(i)+": ")
            f.write(" - delta_" + sw_i + " + " + " + ".join("prob_"+swb for swb in swb_i)+" <= "+str(s_w_probs[i]) + ";\n")
            f.write(" ctswright_"+str(i)+": ")
            f.write(" delta_" + sw_i + " + " + " + ".join("prob_"+swb for swb in swb_i)+" >= "+str(s_w_probs[i]) + ";\n")
        slate_size = len([int(s) for s in ((s_w[0].split('_'))[0].split('.'))[:-1]])
        f.write(" ct_sumprobs: ")
        f.write(" + ".join("prob_"+''.join(str(b) for b in bucket) for bucket in bucket_orders))
        f.write(" = 1;\n")
        f.write("Bounds\n")
        for bucket in bucket_orders:
            bkt = ''.join(str(b) for b in bucket)
            f.write(" prob_" + bkt + " >= 0\n")
        f.write("End\n")


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
            lines.append(row[1:])
    return name_file, slate_size, lines

def slates_with_winners(slates):
    slates_winners_dict = defaultdict(list)
    for s in slates:
        slates_winners_dict['.'.join(s[:-1])].append(s[-1])
    return slates_winners_dict

def slates_winners_probs(slates_dict):
    slates_probs_dict = defaultdict(float)
    for slate,winners in slates_dict.items():
        slate_probs = defaultdict(float)
        num_winners = len(winners)
        for w in winners:
            slate_probs[w]+=1.0/num_winners
        for w in slate_probs:
            slates_probs_dict[slate+'_'+w] = slate_probs[w]
    return slates_probs_dict

def slates_with_winner_2_bucket_orders(slates_winners_probs_dict, num_buckets, sample_prob):
    slates_with_winners = []
    s_w_probs = []
    s_w_buckets = []
    bucket_orders = []
    for slate_winner, prob in slates_winners_probs_dict.items():
        s_w_probs.append(prob)
        slates_with_winners.append(slate_winner)
        if not bucket_orders:
            slate_size = len((slate_winner.split('_')[0]).split('.'))-1
            print(slate_size)
            bucket_orders = get_bucket_orders(slate_size, num_buckets, sample_prob)
            print(len(bucket_orders))
        s_w_buckets.append(bucket_orders_from_slate_with_winner(slate_winner, bucket_orders))
    return slates_with_winners, s_w_probs, s_w_buckets, bucket_orders

def get_bucket_orders(num_elems, num_buckets, sample_prob):
    bkts = []
    for bkt in itertools.product(range(num_buckets), repeat=num_elems):
        if sample_prob >= 1.0 or random.random() <= sample_prob:
            bkts.append(bkt)
    return bkts

def bucket_orders_from_slate_with_winner(slate_winner, bucket_orders):
    s_w = slate_winner.split('_')
    slate = [int(s) for s in (s_w[0].split('.'))[:-1]]
    slate_size = len(slate)
    winner = int(s_w[1])-1
    nochoice = False
    if winner == slate_size:
        nochoice = True
    feasible_buckets = [] # below range(h) -> h-bucket orders.
    for bucket in bucket_orders:
        if nochoice:
            bs_prod = [bucket[i]*slate[i] for i in range(slate_size)]
            num_max_elems = len([bs for bs in bs_prod if bs==max(bs_prod)])
            if num_max_elems > 1:
                bkt = ''.join(str(b) for b in bucket)
                feasible_buckets.append(bkt)
        else:
            winner_score = bucket[winner]
            others_score = max(bucket[i]*slate[i] for i in range(slate_size) if i!=winner)
            if winner_score > others_score:
                bkt = ''.join(str(b) for b in bucket)
                feasible_buckets.append(bkt)
    return feasible_buckets


parser = argparse.ArgumentParser()
parser.add_argument("f", nargs="+")
parser.add_argument("--basedir", default="./lp")
parser.add_argument("--seed", type=int, default=42)
parser.add_argument("--numbuckets", type=int, default=2)
parser.add_argument("--sampleprob", type=float, default=1.0)

args = parser.parse_args()

for f in args.f:
    print(f)
    name_file, slate_size, slates = parse_slates(f)
    delta = float(name_file.split('_')[-1])
    random.seed(args.seed)
    print(name_file)
    slates_winners_dict = slates_with_winners(slates)
    slates.clear()  # just to save memory
    slates_winners_probs_dict = slates_winners_probs(slates_winners_dict)
    s_w, s_w_probs, s_w_buckets, bucket_orders = slates_with_winner_2_bucket_orders(slates_winners_probs_dict, args.numbuckets, args.sampleprob)
    print(len(s_w))
    """
    fout_dat = f"{args.basedir}/{name_file}_lp.dat"
    save_lp_dat(fout_dat, s_w, s_w_probs)
    fout_mod = f"{args.basedir}/{name_file}_lp.mod"
    save_lp_mod(fout_mod, s_w_buckets)
    """
    fout_lp = f"{args.basedir}/{name_file}.lp"
    save_lp(fout_lp, s_w, s_w_probs, s_w_buckets, bucket_orders)
    