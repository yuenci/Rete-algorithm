'''
Author: Innis
Description: use for rete algorithm
Date: 2022-03-31 11:32:02
LastEditTime: 2022-03-31 13:45:13
FilePath: \0328P-rete\0.3\vertex_multi_rule.py
'''

from typing import Union, List
from pprint import pprint

class Alpha:
    def __init__(self,pattern:str) ->None:
        self.pattern = pattern
        self.edges = {}
        self.activated_state =False

    def add_edge(self,beta_node_obj:object,weight=0) ->None:
        self.edge[beta_node_obj] =weight

    def set_activated_state(self,state:bool)->None:
        self.activated_state = state

    def get_activated_state(self)->bool:
        return self.activated_state

class Beta:
    def __init__(self,left_node:object,right_node:object) -> None:
        self.activated_state = False

        self.left_node = left_node
        self.right_node = right_node
        self.adjacent_beta_node = {}

        self.action = None

    def set_left_node(self,left_node:object)->None:
        self.left_node = left_node

    def set_rigth_node(self,right_node:object)->None:
        self.right_node = right_node

    def get_left_node(self)->object:
        return self.left_node

    def get_rigth_node(self)->object:
        return self.right_node

    def add_adjacent_beta_node(self,beta_node_obj:object,weight=0) ->None:
        self.adjacent_beta_node[beta_node_obj] =weight

    def set_activated_state(self,state:bool)->None:
        self.activated_state = state

    def get_activated_state(self)->bool:
        return self.activated_state

    def set_action(self,action:any)->None:
        self.action = action

class Graph:
    def __init__(self)->None:
        self.graph_alpha_dict = {}
        self.graph_beta_dict = {}

    def add_alpha_node(self, alpha_node:object)->None:
        self.graph_alpha_dict[alpha_node.pattern] = alpha_node


    def add_beta_node(self, beta_node:object)->None:
        self.graph_beta_dict[beta_node.pattern] = beta_node

    def add_rule(self,rule:str)->None:
        pattern:List[str] = [ele for ele in rule.split(" ") if ele != "if"][:-2]
        pattern = sorted(pattern)
        alpha_nodes_List:List[object] = []
        beta_nodes_List:List[object] = []

        #Create alpha nodes, if there is exist, use exist one.
        for ele in pattern:
            alpha_object = Alpha(ele)
            alpha_nodes_List.append(alpha_object)

        #Create beta nodes , if there is exist, use exist one.
        for index in range(1,len(alpha_nodes_List)):
            if index == 1:
                beta_object = Beta(alpha_nodes_List[index-1],alpha_nodes_List[index])
            else:
                beta_object = Beta(beta_nodes_List[index-2],alpha_nodes_List[index])
            beta_nodes_List.append(beta_object)

        #Set each alpha node link with beta node
        for index in range(len(alpha_nodes_List)):
            if index==0:
                alpha_nodes_List[0].set_adjacent_beta_node(beta_nodes_List[0])
            else:
                alpha_nodes_List[index].set_adjacent_beta_node(beta_nodes_List[index-1])

        #Add alpha to graph dict
        for ele in alpha_nodes_List:
            self.add_alpha_node(ele)

        #Add beta nodes to graph dict
        for index in range(len(beta_nodes_List)):
            beta_pattern = "-".join(pattern[:index+2])
            beta_nodes_List[index].set_pattern(beta_pattern)
            self.add_beta_node(beta_nodes_List[index])




    def match(*patterns:str)->Union[str,bool]:
        pass

### test
rule1: str = "if a1 b1 c1 d1 e1 then action1"
rule2: str = "if a2 b2 c2 d2 e2 then action2"
rule3: str = "if a1 b2 c1 d2 e1 then action3"
rule4: str = "if a2 b1 c2 d1 e2 then action4"
rule5: str = "if a2 b1 c3 d1 e5 then action5"
rules = [rule1,rule2,rule3,rule4,rule5]

rete = Graph()
for ele in rules:
    rete.add_rule(ele)
pprint(rete.graph_alpha_dict)
pprint(rete.graph_beta_dict)

