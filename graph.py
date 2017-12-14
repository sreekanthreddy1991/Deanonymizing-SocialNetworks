import networkx as nx
import math
import random
from random import randint
fh = open("D:\Studies\Advanced Algorithm\project\dataset\com-lj.ungraph.txt", "r")
path = "D:\Studies\Advanced Algorithm\project\dataset\com-lj.ungraph.txt"
path2 = "facebook_combined.txt"
path3 = "com-dblp.ungraph.txt"
g = nx.read_edgelist(path3,comments="#" ,create_using=nx.Graph(), nodetype=int)
print(nx.info(g))
new_nodes_length = math.log(len(g), 2)
new_nodes_length = math.ceil(new_nodes_length*2.2)
new_nodes = []
g_len = len(g)
print("new length", new_nodes_length)
# print(new_nodes)
for num in range(0, new_nodes_length):
    new_node = g_len+num
    # print(new_node)
    g.add_node(new_node)
    new_nodes.append(new_node)
print(nx.info(g))
# print(new_nodes_length, len(new_nodes))
for i in new_nodes:
    print(g.has_node(i))
target_node_length = new_nodes_length
target_nodes = []
while(len(target_nodes)<target_node_length):
    l = randint(0, g_len-1)
    if(l not in target_nodes):
        target_nodes.append(l)
new_node_degree = {}
for num in new_nodes:
    new_node_degree[num] = randint(3,4)
# print(new_node_degree)
target_nodes_degree = {}
for num in target_nodes:
    target_nodes_degree[num] = randint(2, 3)
# print(target_nodes_degree)
target_nodes_edges = {}
picked_combinations = []
def pick_combination(node_set, start_range, end_range, picked_combinations):
    edge_combination = []
    random_set = node_set[:]
    for num in range(start_range, end_range):
        rand = random.choice(random_set)
        edge_combination.append(rand)
        random_set.remove(rand)
    present = True
    for sub_list in picked_combinations:
        present = True
        if(len(edge_combination)==len(sub_list)):
            for mem in sub_list:
                if(mem not in edge_combination):
                    present = False
                    break
        else: present = False
    if(len(picked_combinations)==0):
        present = False
    if(present or edge_combination is None):
        return pick_combination(node_set, start_range, end_range, picked_combinations)
    else:
        return edge_combination
# print(target_nodes_degree)
new_node_edges = {}
new_node_degree_counter = new_node_degree.copy()
nodes_to_pick_from = new_nodes[:]
count = 0
for target in target_nodes:
    edge_combination = pick_combination(nodes_to_pick_from, 0, target_nodes_degree[target], picked_combinations)
    # if edge_combination is None:
    #     print("print Here")
    picked_combinations.append(edge_combination)
    target_nodes_edges[target] = edge_combination
    for mem in edge_combination:
        g.add_edge(target, mem)
        count+=1
        new_node_degree_counter[mem] = new_node_degree_counter[mem]-1
        if(new_node_degree_counter[mem] == 0):
            nodes_to_pick_from.remove(mem)
        edges = []
        if(mem in new_node_edges):
            edges = new_node_edges[mem]
        edges.append(target)
        new_node_edges[mem] = edges
# print(count)
# print(target_nodes_edges)
# print(new_node_degree)
# print(new_node_edges)
extra_target_nodes = []
def adding_extra_edges_to_new_nodes(numEdges, end_range, target_nodes, extra_nodes):
    node_list = []
    add = True
    count = 0
    while(add):
        extra_node = randint(0, end_range)
        if ((extra_node in target_nodes) or (extra_node in extra_nodes)):
            continue
        else:
            node_list.append(extra_node)
            count = count+1
        if(count == numEdges): add = False
    return node_list

for new_node in new_node_degree_counter:
    if(new_node_degree_counter[new_node] > 0):
        node_list = adding_extra_edges_to_new_nodes(new_node_degree_counter[new_node], g_len, target_nodes, extra_target_nodes)
        extra_target_nodes.extend(node_list)
        for node in node_list:
            g.add_edge(node, new_node)
            new_node_degree_counter[new_node] = new_node_degree_counter[new_node] - 1

# adding sequence edges to new nodes
node_count = 0
new_node_internal_degree = {}
print(new_nodes_length)
for node in new_nodes:
    if(node_count < new_nodes_length-1):
        g.add_edge(node, node+1);
        if(node in new_node_internal_degree):
            new_node_internal_degree[node] = new_node_internal_degree[node]+1
        else:
            new_node_internal_degree[node] = 1
    for num in range(node+2, new_nodes[-1]):
        if(node_count<new_nodes_length-2):
            is_random_edge = randint(0,1)
            if(is_random_edge==1):
                g.add_edge(node, num)
                new_node_internal_degree[node] = new_node_internal_degree[node] + 1
    node_count = node_count+1

# print(len(new_node_internal_degree))
# print(new_node_internal_degree)


