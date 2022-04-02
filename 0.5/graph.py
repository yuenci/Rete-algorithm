'''
Author: Innis
Description: graph class and method
Date: 2022-04-02 09:31:06
LastEditTime: 2022-04-02 17:05:52
FilePath: \0328P-rete\0.5\graph.py
'''

from typing import Union, List, Dict
from pprint import pprint
from node import Alpha, Beta
import sys
import time
import json


class Graph:
    def __init__(self) -> None:
        self._graph_alpha_dict: Dict[str, object] = {}
        self._graph_beta_dict: Dict[str, object] = {}

    def add_alpha_inst_to_graph_dict(self, alpha_node_inst: object) -> None:
        self._graph_alpha_dict[alpha_node_inst.get_pattern()] = alpha_node_inst

    def get_graph_alpha_dict(self) -> Dict[str, object]:
        return self._graph_alpha_dict

    def add_beta_inst_to_graph_dict(self, beta_node_inst: object) -> None:
        self._graph_beta_dict[beta_node_inst.get_pattern()] = beta_node_inst

    def get_graph_beta_dict(self) -> Dict[str, object]:
        return self._graph_beta_dict

    def create_alpha_to_graph(self, pattern: str) -> object:
        alpha_inst = Alpha(pattern)
        self.add_alpha_inst_to_graph_dict(alpha_inst)
        return alpha_inst

    def create_beta_to_graph(self, pattern: str, action: str, left_node: object, right_node: object, left_weight: int = 0, right_weight: int = 0) -> object:
        beta_inst = Beta(pattern, action, left_node,
                         right_node, left_weight, right_weight)
        self.add_beta_inst_to_graph_dict(beta_inst)
        return beta_inst

    def check_rule_form(self, rule: str) -> bool:
        if isinstance(rule, str) != True:
            print("not str")
            return False

        eleemnt_list = rule.split(" ")
        if eleemnt_list[0].lower() != "if" or eleemnt_list[-2].lower() != "then":
            print("if then")
            return False

        return True

    def split_rule_pattern_to_list(self, rule: str) -> List[str]:
        pattern: List[str] = [
            ele for ele in rule.split(" ") if ele != "if"][:-2]
        pattern: List[str] = sorted(pattern)
        return pattern

    def get_action_from_rule(self, rule: str) -> str:
        return rule.split(" ")[-1]

    def split_exist_alpha_nodes_and_new_alpha_nodes(self, alpha_nodes_pattern: List[str]) -> List[List[str]]:
        exist_alpha_nodes: List[str] = []
        new_alpha_nodes: List[str] = []
        for ele in alpha_nodes_pattern:
            if ele in self.get_graph_alpha_dict():
                exist_alpha_nodes.append(ele)
            else:
                new_alpha_nodes.append(ele)

        return [sorted(exist_alpha_nodes), sorted(new_alpha_nodes)]

    def get_exist_alpha_node_init_form_pattern(self, alpha_pattern: Union[str, List[str]]) -> List[object]:
        if isinstance(alpha_pattern, str):
            return [self.get_graph_alpha_dict()[alpha_pattern]]
        elif isinstance(alpha_pattern, list):
            alpha_init_list: List[object] = []
            for ele in alpha_pattern:
                alpha_init = self.get_graph_alpha_dict()[ele]
                alpha_init_list.append(alpha_init)
            return alpha_init_list

    def get_duplicates(self, arr: List[object]) -> object:
        hashset = set()
        duplication = []
        for el in arr:
            if el not in hashset:
                hashset.add(el)
            else:
                duplication.append(el)
        return duplication

    def find_the_biggest_beta_node(self, exist_alpha_inst_list: List[object]) -> List[Union[object, List[object]]]:
        exist_alpha_inst_Dict: Dict[str:object] = {}
        for node_inst in exist_alpha_inst_list:
            exist_alpha_inst_Dict[node_inst.get_pattern()] = node_inst

        beta_node_list: List[object] = []
        for ele in exist_alpha_inst_list:
            beta_node_list += ele.get_edge_object_list()

        duplicates: object = self.get_duplicates(beta_node_list)

        # no link
        if len(duplicates) == 0:
            return [None, exist_alpha_inst_list]
        else:
            duplicates = duplicates[0]

        del exist_alpha_inst_Dict[duplicates.get_left_node().get_pattern()]
        del exist_alpha_inst_Dict[duplicates.get_right_node().get_pattern()]

        highest: object = duplicates
        flag = False
        while True:
            higher_beta_inst_list: List[object] = highest.get_edge_object_list(
            )
            for ele in higher_beta_inst_list:
                right_side_node_obj: object = ele.get_right_node()
                right_side_node_pattern: str = right_side_node_obj.get_pattern()
                if right_side_node_pattern in exist_alpha_inst_Dict:
                    highest: object = ele
                    del exist_alpha_inst_Dict[right_side_node_pattern]
                    flag = True
                    break
            if len(exist_alpha_inst_Dict) == 0:
                return [highest, list(exist_alpha_inst_Dict.values())]
            if flag == False:
                return [highest, list(exist_alpha_inst_Dict.values())]
            flag = False

    def connect_net(self, biggest: object, rest_of_alpha_inst_list: List[object], new_pattern: List[str], action: str) -> None:
        new_alpha_inst_list: List[object] = []
        if len(new_pattern) > 0:
            sorted(new_pattern)
            for ele in new_pattern:
                new_alpha_inst_list.append(self.create_alpha_to_graph(ele))

        all_alpha_inst_list: List[object] = rest_of_alpha_inst_list + \
            new_alpha_inst_list
        all_alpha_pattern_list: List[str] = [
            ele.get_pattern() for ele in all_alpha_inst_list]

        temp_beta_node_inst_list: List[object] = [biggest]

        for index in range(len(all_alpha_inst_list)):
            beta_pattern: str = temp_beta_node_inst_list[index].get_pattern(
            ) + "-" + all_alpha_pattern_list[index]

            left_node_init: object = temp_beta_node_inst_list[index]
            right_node_init: object = all_alpha_inst_list[index]

            beta_inst = self.create_beta_to_graph(
                beta_pattern, None, left_node_init, right_node_init)

            temp_beta_node_inst_list.append(beta_inst)
        temp_beta_node_inst_list[-1].set_action(action)

    def build_net(self, biggest: object, rest_of_alpha_inst_list: List[object], new_pattern: List[str], action: str) -> None:
        new_alpha_inst_list: List[object] = []
        if len(new_pattern) > 0:
            sorted(new_pattern)
            for ele in new_pattern:
                new_alpha_inst_list.append(self.create_alpha_to_graph(ele))

        all_alpha_inst_list: List[object] = rest_of_alpha_inst_list + \
            new_alpha_inst_list
        all_alpha_pattern_list: List[str] = [
            ele.get_pattern() for ele in all_alpha_inst_list]

        temp_beta_node_inst_list: List[object] = []

        for index in range(1, len(all_alpha_inst_list)):
            beta_pattern: str = "-".join(all_alpha_pattern_list[:index+1])

            if index == 1:
                left_node_init: object = all_alpha_inst_list[index-1]
                right_node_init: object = all_alpha_inst_list[index]
            else:
                left_node_init: object = temp_beta_node_inst_list[index-2]
                right_node_init: object = all_alpha_inst_list[index]

            beta_inst = self.create_beta_to_graph(
                beta_pattern, None, left_node_init, right_node_init)

            temp_beta_node_inst_list.append(beta_inst)
        temp_beta_node_inst_list[-1].set_action(action)

    def add_rule(self, rule: str) -> None:
        action: str = self.get_action_from_rule(rule)
        pattern_list: List[str] = self.split_rule_pattern_to_list(rule)
        exist_alpha_pattern_list, new_pattern_list = self.split_exist_alpha_nodes_and_new_alpha_nodes(
            pattern_list)

        if len(new_pattern_list) > 0 and len(exist_alpha_pattern_list) == 0:
            '''
            all are new pattern
            need to build new net
            '''
            exist_alpha_node_inst_list: List[object] = self.get_exist_alpha_node_init_form_pattern(
                exist_alpha_pattern_list)
            self.build_net(None, [], pattern_list, action)
        # all are old pattern
        elif len(new_pattern_list) == 0 and len(exist_alpha_pattern_list) > 0:
            exist_alpha_node_inst_list: List[object] = self.get_exist_alpha_node_init_form_pattern(
                exist_alpha_pattern_list)
            biggest_beta_node_inst: object
            except_biggest_the_rest_of_alpha_inst: List[object]
            biggest_beta_node_inst, except_biggest_the_rest_of_alpha_inst = self.find_the_biggest_beta_node(
                exist_alpha_node_inst_list)

            if biggest_beta_node_inst == None:
                '''
                all are old pattern and no biggest
                need to build new net
                '''
                self.build_net(None, exist_alpha_node_inst_list, [], action)
            else:
                if len(except_biggest_the_rest_of_alpha_inst) == 0:
                    '''
                    all are old pattern and has biggest and no left
                    🚨 there have conflictd
                    '''
                else:
                    '''
                    all are old pattern and has biggest and left
                    need to use biggest and the rest alpha nodes  build new net
                    '''
                    self.connect_net(biggest_beta_node_inst,
                                     except_biggest_the_rest_of_alpha_inst, [], action)
        # there are old pattern and new pattern
        elif len(new_pattern_list) > 0 and len(exist_alpha_pattern_list) > 0:
            exist_alpha_node_inst_list: List[object] = self.get_exist_alpha_node_init_form_pattern(
                exist_alpha_pattern_list)
            biggest_beta_node_inst: object
            except_biggest_the_rest_of_alpha_inst: List[object]
            biggest_beta_node_inst, except_biggest_the_rest_of_alpha_inst = self.find_the_biggest_beta_node(
                exist_alpha_node_inst_list)

            if biggest_beta_node_inst == None:
                '''
                there are old pattern , new pattern and no biggest
                need to ues old pattern , new pattern build new net
                '''
                self.build_net(
                    None, except_biggest_the_rest_of_alpha_inst, new_pattern_list, action)
            # all are old pattern and has biggest
            else:
                if len(except_biggest_the_rest_of_alpha_inst) == 0:
                    '''
                    there are old pattern , new pattern and has biggest and no left
                    ues biggest and  new pattern build new net
                    '''
                    self.connect_net(biggest_beta_node_inst,
                                     [], new_pattern_list, action)
                else:
                    '''
                    there are old pattern , new pattern and has biggest and left
                    need to use biggest ,the rest alpha nodes new pattern  build new net
                    '''
                    self.connect_net(biggest_beta_node_inst,
                                     except_biggest_the_rest_of_alpha_inst, new_pattern_list, action)

        else:
            raise Exception(f"This rule has some problem: {rule}")

    def query(self, rule: str) -> str:

        pattern_list: List = sorted(rule.strip().split(" "))
        # if hvae duplicates
        if len(self.get_duplicates(pattern_list)) > 0:
            raise Exception(f"This rule has repetitive pattern: {rule}")

        # if all pattern exist
        for ele in pattern_list:
            if ele not in self.get_graph_alpha_dict():
                return None
        exist_alpha_inst = self.get_exist_alpha_node_init_form_pattern(
            pattern_list)

        biggest = self.find_the_biggest_beta_node(exist_alpha_inst)
        if biggest == None:
            return None
        else:
            return biggest[0].get_action()

    def export_graph_data(self) -> None:
        graph_data_dict = {"alpha": {}, "beta": {}}

        all_ahpha_pattern: List[str] = list(self.get_graph_alpha_dict().keys())
        all_ahpha_inst: List[object] = list(self.get_graph_alpha_dict().values()
                                            )
        for index in range(len(all_ahpha_pattern)):
            graph_data_dict["alpha"][all_ahpha_pattern[index]
                                     ] = all_ahpha_inst[index].get_edge_pattern_weight_dict()

        all_beta_pattern: List[str] = list(self.get_graph_beta_dict().keys())
        all_beta_inst: List[object] = list(self.get_graph_beta_dict().values())

        for index in range(len(all_beta_pattern)):
            graph_data_dict["beta"][all_beta_pattern[index]] = {
                "action": all_beta_inst[index].get_action(),
                "left_node": all_beta_inst[index].get_left_node().get_pattern(),
                "right_node": all_beta_inst[index].get_right_node().get_pattern(),
                "edge": all_beta_inst[index].get_edge_pattern_weight_dict()
            }

        with open("data.json", "w+") as handle:
            json.dump(graph_data_dict, handle, ensure_ascii=False)


####
rule1: str = "if a1 b1 c1 d1 e1 then action111"
rule2: str = "if a1 b1 c1 d2 e2 then action222"
rule3: str = "if d1 e1 d2 e2 then action333"
rule4: str = "if a1 b1 d2 e2 then action444"
rule5: str = "if a11 b11 d21 e21 then action555"


rete = Graph()

# region small test data
rete.add_rule(rule1)
rete.add_rule(rule2)
rete.add_rule(rule3)
rete.add_rule(rule4)
rete.add_rule(rule5)

rete.export_graph_data()

# print("alpha nodes")
#print("beta nodes")
# pprint(rete._graph_beta_dict)

# print(rete.query("a1 c1 b1 e1 d1 "))
# endregion

# start = time.time()
# with open("data.txt", "r") as handle:
#     rules = handle.readlines()


# times = 0
# st = time.time()
# for index in range(1000):
#     rete.add_rule(rules[index].strip())
#     if index % 1000 == 0:
#         en = time.time()
#         print(f"{times},cost:{en-st} s")
#         st = time.time()
#     times += 1

# end = time.time()
# print(f"Bulid graph cost {end-start}s")


# start = time.time()
# print(rete.query("a9 b9 c9 d9 e9 f0"))
# end = time.time()

# print(f"rete query cost {end-start}s")

# st = time.time()
# for ele in rules:
#     if ele.strip() == "if a9 b9 c9 d9 e9 f0 then action99999":
#         print(ele.strip().split(" ")[-1])
# en = time.time()

# print(f"traverse query cost:{en-st}s")
