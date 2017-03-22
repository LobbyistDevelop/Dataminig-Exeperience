import itertools
import sys

#get support of item_set by trax_list
def get_support(trax_list, item_set):
    support = 0
    for trax in trax_list :
        flag = True
        for item in item_set :
            if item not in trax :
                flag = False
                break
        if flag :
            support = support + 1
    return support

# generate frequents by testing cantidates by trax_list, condition is candidate's support >= min_sup
def get_frequents(trax_list, candidates, min_sup):
    frequents = dict()
    for item_set in candidates:
        sup = get_support(trax_list, item_set)
        if sup >= min_sup :
            frequents[tuple(sorted(item_set))] = sup
    return frequents

#get command line arguments and store
arg_min_sup = float(sys.argv[1])
arg_input_file_name = sys.argv[2]
arg_output_file_name = sys.argv[3]

min_sup = 0
trax_list = [] #tranx_list is list of transactions. form : [(0,1,3), (trax itemset), ...}
freq_index = 1 #freq_index, frequents[i] means i-itemsets(frequents[3] -> 3-itemsets)
candidates = set() # set of candidate item tuples, form : {(0,1), (1,3), (itemset), ...}
frequents = dict() # dict of dict {frequent-itemset : support}. form : { 1 : { {(1,) : 40, (2,) : 120, ...}, 2: { (2,3) : 30, (4,5) : 50 },...}
                                                                #   ( {freq_index : { (frequent-item set : support }, ...}

#read input file and initiate trax_list
input_file = open(arg_input_file_name, 'r')
line = input_file.readline()
while line :
    line =  line.strip('\n');
    trax_list.append(tuple(map(lambda x : int(x), line.split('\t'))))
    line = input_file.readline()

min_sup = len(trax_list) * (arg_min_sup/float(100))# convert persent to number

#init the 1-itemset candidates
for trax in trax_list:
    candidates |= {(item,) for item in trax}

#get 1item-set frequent
frequents[freq_index] = get_frequents(trax_list, candidates, min_sup)

#main code of this algorithm
#build frequents dict
while frequents[freq_index] : # until current level frequent-set is empty
    items_sets = frequents[freq_index].keys() #values are support, we need only item_set
    candidates = set() # candidate of next level
    for set1 in items_sets:
        flag = False
        for set2 in items_sets:
            if set1 == set2:#this flag is for blocking redundancy, every set2 before set1 is joined
                flag = True
            if not flag :
                continue
            cand = tuple(sorted(set(set1+set2))) #for using itemset as key of dicionary, it must be tuple and sorted
            if len(cand) == freq_index+1:# next level candidates is registered to candidates
                candidates |= {cand}
    frequents[freq_index + 1] = get_frequents(trax_list, candidates, min_sup) #generate nex level frequents
    freq_index = freq_index + 1 #to next level

#print to output.txt
try :
    with open(arg_output_file_name, 'w') as f:
        for freq_index in range(2, len(frequents)):
            for item_set in frequents[freq_index].keys():
                item_set_sup = frequents[freq_index][item_set]
                for item_subset_size in range(1, len(item_set)):
                    for item_subset in itertools.combinations(item_set, item_subset_size) :
                        item_subset_sup = frequents[item_subset_size][item_subset]
                        confidence = item_set_sup / float(item_subset_sup) * 100
                        f.write('{')
                        for item in item_subset :
                            f.write(str(item)+',')
                        f.seek(-1, 1) #delete one comma

                        f.write('}\t{')
                        for item in item_set :
                            if item not in item_subset :
                                f.write(str(item)+',')
                        f.seek(-1, 1)
                        f.write('}\t%.2f\t%.2f\n'%(item_set_sup/float(len(trax_list)) * 100, confidence))
except :
    print "can't write the ouput.txt file."



