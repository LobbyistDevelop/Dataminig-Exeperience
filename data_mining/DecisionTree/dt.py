import math
import sys
train_file_name = sys.argv[1]
test_file_name = sys.argv[2]
result_file_name = 'dt_result.txt'

test_tuples = []
examples = []
attributes = dict()     #attribute is dict{integer value(representing each attribute) : {value1, value2, ...}, ...}
classes = {}
example_attributes_name = []
with open(train_file_name) as train_file :
    example_attributes_name = train_file.readline().split()
    attributes = {att : set() for att in xrange(0, len(example_attributes_name))}    #except class
    for line in train_file:
        t = line.split()
        examples.append(t)
        for i, value in enumerate(t):
            attributes[i].add(value)
    classes = attributes[len(attributes)-1]
    del attributes[len(attributes)-1]

with open(test_file_name) as test_file :
    test_attributes_name = test_file.readline().split()
    for line in test_file :
        test_tuples.append(line.split())

class Node :
    def __init__(self, attriubute, children= None, isLeaf=False):
        self.isLeaf = isLeaf     #if leaf, attribute is class
        self.attribute = attriubute     
        if children is None:
            self.children = {}
        else:
            self.children = children      #dict{ edge : node, ...}


def majority_class(examples):
    classes = dict()
    majority = examples[0][-1]
    for example in examples:
        try :
            classes[example[-1]] += 1
        except KeyError as e:
            classes[example[-1]] = 1
    max = 0
    sum = 0
    for k, v in classes.iteritems():
        sum += v
        if v > max :
            majority = k
            max = v
    return majority, classes[majority]/float(sum)


def has_same_class(examples):
    test_class = examples[0][-1]
    for example in examples:
        if test_class != example[-1]:
            return False
    return True


def information_content(cnt_per_class):     # list of count per each class
    entire_size = sum(cnt_per_class)
    return sum(-(cnt / float(entire_size))*math.log(cnt/float(entire_size), 2) for cnt in cnt_per_class if cnt != 0)


def select_best_att(examples, attributes, classes):                  # return attribute which has the lowest remaainder value
    remainders = dict()         # remainder per each attribute { remainder : attribute, ...}
    # classes = attributes[len(attributes)-1]
    example_size = len(examples)
    for i in attributes.keys(): # last item is not an attribute, but the class
        remainder = 0
        for att_value in attributes[i] :
            sub_example_for_value = filter(lambda e : e[i] == att_value, examples)
            sub_example_size = len(sub_example_for_value)
            weight = float(sub_example_size)/example_size
            cnt_per_class = []
            for data_class in classes:
                cnt_per_class.append(sum( e[-1] == data_class for e in sub_example_for_value)) # count of class for each value of the attribtue
            remainder += weight * information_content(cnt_per_class)
        remainders[remainder] = i
    best_attribute = remainders[min(remainders.keys())]
    return best_attribute, attributes[best_attribute]


def decision_tree_learn(examples, attributes, classes, pruning_threshold):
    if not examples:    #len(attributes) == 1 means only class exist.
        return None
    if has_same_class(examples):                #all of datas has same class
        return Node(examples[0][-1], None, True)
    major_class, majority_rate = majority_class(examples)
    if not attributes :     #if example is not empty and attrivutes is empty
        return Node(major_class, None, True)
    if 1-majority_rate <= pruning_threshold :     #pruning
        return Node(major_class, None, True)

    best_attribute, values = select_best_att(examples, attributes, classes)
    node = Node(best_attribute)
    sub_attributes = attributes.copy()
    del sub_attributes[best_attribute]

    for value in values :
        node.children[value] = decision_tree_learn(
                filter(lambda e : e[best_attribute] == value , examples),
                sub_attributes, classes, pruning_threshold)
    return node
    #attributes.remove(best_attribute)

def predict_class_by_decision_tree(tuple, decision_tree):
    if decision_tree is None :      # None node means the tuple is not trained data (way to improve parent majority calss)
        random_class = classes.pop()
        classes.add(random_class)
        return random_class
    if decision_tree.isLeaf :
        return decision_tree.attribute
    return predict_class_by_decision_tree(tuple, decision_tree.children[tuple[decision_tree.attribute]])


decision_tree = decision_tree_learn(examples, attributes, classes, 0)

with open(result_file_name, 'w') as result_file :
    for att_name in example_attributes_name :
        result_file.write(att_name + '\t')
    result_file.write('\n')
    for tuple in test_tuples:
        for value in tuple :
            result_file.write(value + '\t')
        result_file.write(predict_class_by_decision_tree(tuple, decision_tree)+'\n')




