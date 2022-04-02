'''
Author: Innis
Description: graph class and method
Date: 2022-04-02 09:31:06
LastEditTime: 2022-04-02 12:25:49
FilePath: \0328P-rete\0.5\graph.py
'''

from typing import Union, List, Dict
from pprint import pprint
from node import Alpha, Beta
import sys


class Graph:
    def __init__(self) -> None:
        self._graph_alpha_dict: Dict[str, object] = {}
        self._graph_beta_dict: Dict[str, object] = {}

    def add_alpha_inst_to_graph_dict(self, alpha_node_inst: object) -> None:
        self._graph_alpha_dict[alpha_node_inst.get_pattern()] = [
            alpha_node_inst]

    def get_graph_alpha_dict(self) -> Dict[str, object]:
        return self._graph_alpha_dict

    def add_beta_inst_to_graph_dict(self, beta_node_inst: object) -> None:
        self._graph_beta_dict[beta_node_inst.get_pattern()] = [
            beta_node_inst]

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
        pprint(exist_alpha_inst_list)
        print(sys._getframe().f_lineno, "line")
        for node_inst in exist_alpha_inst_list:
            exist_alpha_inst_Dict[node_inst.get_pattern()] = node_inst

        beta_node_list: List[object] = []
        for ele in exist_alpha_inst_list:
            beta_node_list += ele.get_edge_object_list()

        duplicates: object = self.get_duplicates(beta_node_list)

        # no link
        if len(duplicates) == 0:
            return [None, []]
        else:
            duplicates = duplicates[0]

        del exist_alpha_inst_Dict[duplicates.get_left_node().get_pattern()]
        del exist_alpha_inst_Dict[duplicates.get_rigth_node().get_pattern()]

        highest: object = duplicates
        flag = False
        while True:
            higher_beta_inst_list: List[object] = highest.get_edge_object_list(
            )
            for ele in higher_beta_inst_list:
                right_side_node_obj: object = ele.get_rigth_node()
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
            ) + all_alpha_pattern_list[index]

            left_node_init: object = temp_beta_node_inst_list[index]
            right_node_init: object = all_alpha_inst_list[index]

            beta_inst = self.create_beta_to_graph(
                beta_pattern, action, left_node_init, right_node_init)

            temp_beta_node_inst_list.append(beta_inst)

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
                beta_pattern, action, left_node_init, right_node_init)

            temp_beta_node_inst_list.append(beta_inst)

    def add_rule(self, rule: str) -> None:
        action: str = self.get_action_from_rule(rule)
        pattern_list: List[str] = self.split_rule_pattern_to_list(rule)
        exist_alpha_pattern_list, new_pattern_list = self.split_exist_alpha_nodes_and_new_alpha_nodes(
            pattern_list)

        if len(new_pattern_list) > 0 and len(exist_alpha_pattern_list) == 0:
            '''
            all are new pattern,input:List[str]
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
                all are old pattern and no biggest,input:List[object]
                need to build new net
                '''
                self.build_net(None, exist_alpha_node_inst_list, [], action)
            else:
                print("all are old pattern and has biggest")
                if len(except_biggest_the_rest_of_alpha_inst) == 0:
                    '''
                    all are old pattern and has biggest and no left
                    🚨 there have conflictd
                    '''
                else:
                    '''
                    all are old pattern and has biggest and left,input:List[object,List[object]]
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
                print("all are old pattern and has biggest")
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


####
rule1: str = "if a1 b1 c1 d1 e1 then action111"
rule2: str = "if a1 b1 c1 d2 e2 then action222"
rule3: str = "if d1 e1 d2 e2 then action333"
rule4: str = "if a1 b1 d2 e2 then action444"
rule5: str = "if a11 b11 d21 e21 then action555"


rete = Graph()
rete.add_rule(rule1)


print("alpha nodes")
pprint(rete.get_graph_alpha_dict())
print("beta nodes")
pprint(rete._graph_beta_dict)
