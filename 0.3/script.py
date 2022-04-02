"""
Author: Innis
Description: 
Date: 2022-03-31 13:44:08
LastEditTime: 2022-04-01 09:21:27
FilePath: \0328P-rete\script.py
"""

# built graph
from node import Alpha, Beta
from graph import Graph
from animation import Window
from typing import Union, List
from pprint import pprint
import pygame
rule1: str = "if a1 b1 c1 d1 e1 then action1"
rule2: str = "if a2 b2 c2 d2 e2 then action2"
rule3: str = "if a1 b2 c1 d2 e1 then action3"
rule4: str = "if a2 b1 c2 d1 e2 then action4"
rule5: str = "if a2 b1 c3 d1 e5 then action5"
rules = [rule1, rule2, rule3, rule4, rule5]

rete = Graph()


# for ele in rules:
#     rete.add_rule(ele)


# Visualization part
window = Window(1200, 800)
window.conf()

alpha_node_pattern_list = []


def add_alpha(rule, list=alpha_node_pattern_list):
    rete.add_alpha_node_to_graph(rule)
    rete.add_beta_node_to_graph()
    pattern_list = [ele for ele in rule.split(" ") if ele != "if"][:-2]
    list += pattern_list
    # print(alpha_node_pattern_list)


add_alpha(rule1)
# add_alpha(rule5)
# pprint(rete.graph_alpha_dict)

# region alpha_edge_test
# for ele in rete.graph_alpha_dict.values():
#     pprint(f"{ele.pattern} 's edges:")
#     for ele in ele.edges.keys():
#         pprint(ele.pattern)
#     print("\n")
# endregion


for ele in rete.graph_beta_dict.values():
    pprint(f"{ele.pattern} 's foot:")
    pprint(f"left:{ele.left_node.pattern},right:{ele.right_node.pattern}")
    for el in ele.edges.keys():
        pprint(el.pattern)
    print("\n")


# pprint(rete.graph_beta_dict)

# window.add_alpha_node("3")
# window.add_alpha_node("4")
# window.add_alpha_node("5")
# window.add_beta_node("1-2","1","alpha","2","alpha")
# window.add_beta_node("1-2-3","1-2","beta","3","alpha")
# window.add_beta_node("1-2-3-4","1-2-3","beta","4","alpha")
# window.add_beta_node("1-2-3-4-5","1-2-3-4","beta","5","alpha")
# window.add_alpha_node("6")
# window.add_beta_node("1-2-6","1-2","beta","6","alpha")


# pprint(rete.graph_alpha_dict)
# pprint(rete.graph_beta_dict)

clock = pygame.time.Clock()
while True:
    clock.tick(3)
    if len(alpha_node_pattern_list) > 0:
        alpha_node = alpha_node_pattern_list.pop(0)
        window.add_alpha_node(alpha_node)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
