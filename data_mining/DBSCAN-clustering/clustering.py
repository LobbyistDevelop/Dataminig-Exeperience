#-*- coding:utf-8 -*-
import sys
import math
import re


class Object :
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.is_visit = False

    def __repr__(self):
        return str((self.id, self.x, self.y))

    def __eq__(self, other):
        return self.id == other.id

    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

arg_input_file_name = sys.argv[1]
arg_num_cluster  = int(sys.argv[2])

test_number = int(re.findall(r'\d+', arg_input_file_name)[0])
output_file_name = 'output{0}_cluster_{1}.txt'
objects = []
clusters = []
noises = []

#default
min_pts = 5
eps = 5
if test_number == 1:
    min_pts = 24
    eps = 14.9
elif test_number == 2:
    min_pts = 10
    eps = 2
elif test_number == 3:
    min_pts = 10
    eps = 7

print min_pts, eps

with open(arg_input_file_name, 'r') as f :
    for line in f :
        obj = Object(*map(float, line.split()))
        objects.append(obj)


def make_cluster(cluster, neighbors):
    while neighbors :
        obj = neighbors.pop()
        if obj.is_visit :
            continue
        obj.is_visit = True
        local_neighbors = filter(lambda oth : obj.distance(oth) <= eps, objects)
        if len(local_neighbors) >= min_pts-1 : #core
            neighbors += filter(lambda o : not o.is_visit, local_neighbors)
        cluster += [obj]


eps_change_amount = 0.5     # properly decrease?
while True:
    for obj in objects:
        if obj.is_visit:
            continue
        obj.is_visit = True
        neighbors = filter(lambda oth : obj.distance(oth) <= eps, filter(lambda o : not o.is_visit, objects))
        if len(neighbors) < min_pts-1: # 자기 자신까지 계산해야 하므로 -1
            pass
            # noises.append(obj)
        else :
            cluster = [obj]
            make_cluster(cluster, neighbors)
            clusters += [cluster]
    print len(clusters), arg_num_cluster, eps
    if arg_num_cluster <= len(clusters) <= arg_num_cluster+3:
        break
    if len(clusters) >= arg_num_cluster :
        eps += eps_change_amount
    else:
        eps -= eps_change_amount
    clusters = []
    for obj in objects :
        obj.is_visit = False


for i, cluster in enumerate(clusters[:arg_num_cluster]):
    with open(output_file_name.format(test_number, i), 'w') as f:
        for obj in cluster :
            f.write(str(int(obj.id))+'\n')
