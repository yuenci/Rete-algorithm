'''
Author: Innis
Description: run the rete algorithm
Date: 2022-04-01 14:26:01
LastEditTime: 2022-04-01 22:31:56
FilePath: \0328P-rete\0.4\script.py
'''

from node import Alpha, Beta
from graph import Graph
from typing import Union, List
from pprint import pprint
# import pygame
rule1: str = "if a1 b1 c1 d1 e1 then action1"
rule2: str = "if a2 b2 c2 d2 e2 then action2"
rule3: str = "if a1 b1 c1 d2 e2 then action3"
rule4: str = "if a2 b1 c2 d1 e2 then action4"
rule5: str = "if a2 b1 c3 d1 e5 then action5"
rules = [rule1, rule2, rule3, rule4, rule5]

rete = Graph()
# rete.first_time_add_alpha_node(rule1)

# pprint(rete.get_alpha_inst_temp_list())
# pprint(rete.get_graph_alpha_dict())

# rete.first_time_add_beta_node()

# pprint(rete.get_alpha_inst_temp_list())
# pprint(rete._graph_beta_dict)

# rete.add_alpha_node(rule3)
# pprint(rete.get_alpha_inst_temp_list())
# pprint(rete.get_graph_alpha_dict())
# rete.add_beta_node()


def add_node(rule: str) -> None:
    rete.add_alpha_node(rule)
    rete.add_beta_node()
#print("alpha nodes")
# pprint(rete.get_graph_alpha_dict())
#print("beta nodes")
# pprint(rete._graph_beta_dict)


# add_node("if d1 e1 d2 e2 then action5")
# add_node("if a1 b1 d2 e2 then action66")
# add_node("if a11 b11 d21 e21 then action666")
# # pprint(rete._graph_beta_dict)


# print("alpha nodes")
# pprint(rete.get_graph_alpha_dict())
# print("beta nodes")
# pprint(rete._graph_beta_dict)

with open("data.txt", "r") as handle:
    rules = handle.readlines()

for index in range(3):
    if index == 0:
        rete.first_time_add_alpha_node(rules[0])
        rete.first_time_add_beta_node()
    else:
        add_node(rules[index])
    print(index)
# print("alpha nodes")
# pprint(rete.get_graph_alpha_dict())
# print("beta nodes")
# pprint(rete._graph_beta_dict)
