'''
Author: Innis
Description: graph class.
Date: 2022-04-01 14:12:32
LastEditTime: 2022-04-02 09:33:38
FilePath: \0328P-rete\0.4\graph.py
'''
from typing import Union, List, Dict
from pprint import pprint
from node import Alpha, Beta
import sys


class Graph:
    def __init__(self) -> None:
        self._graph_alpha_dict: Dict[str, object] = {}
        self._alpha_temp_list: List[object] = []
        self._alpha_pattern_temp_list: List[List[str]] = []

        self._rule: str = ""

        self._graph_beta_dict: Dict[str, object] = {}

    def add_alpha_inst_to_graph_dict(self, alpha_node_inst: object) -> None:
        self._graph_alpha_dict[alpha_node_inst.get_pattern()] = [
            alpha_node_inst]

    def get_graph_alpha_dict(self) -> Dict[str, object]:
        return self._graph_alpha_dict

    def add_alpha_inst_to_temp_list(self, alpha_node_inst: object) -> None:
        self._alpha_temp_list.append(alpha_node_inst)

    def get_alpha_inst_temp_list(self) -> None:
        return self._alpha_temp_list

    def empty_alpha_inst_temp_list(self) -> None:
        self._alpha_temp_list = []

    def add_beta_inst_to_graph_dict(self, beta_node_inst: object) -> None:
        self._graph_beta_dict[beta_node_inst.get_pattern()] = [
            beta_node_inst]

    def check_rule_form(self, rule: str) -> bool:
        if isinstance(rule, str) != True:
            print("not str")
            return False

        eleemnt_list = rule.split(" ")
        if eleemnt_list[0].lower() != "if" or eleemnt_list[-2].lower() != "then":
            print("if then")
            return False

        return True

    def notify_nodes_add_edge(self, original_beta_node: object, left_node_inst: object, right_node_inst: object) -> None:
        left_node_inst.add_edge(original_beta_node)
        right_node_inst.add_edge(original_beta_node)

    def split_rule_pattern_to_list(self, rule: str) -> List[str]:
        pattern: List[str] = [
            ele for ele in rule.split(" ") if ele != "if"][:-2]
        pattern: List[str] = sorted(pattern)
        return pattern

    def split_exist_alpha_nodes_and_new_alpha_nodes(self, alpha_nodes_pattern: List[str]) -> List[List[str]]:
        exist_alpha_nodes: List[str] = []
        new_alpha_nodes: List[str] = []
        for ele in alpha_nodes_pattern:
            if ele in self.get_graph_alpha_dict():
                exist_alpha_nodes.append(ele)
            else:
                new_alpha_nodes.append(ele)

        return [sorted(exist_alpha_nodes), sorted(new_alpha_nodes)]

    def get_alpha_node_init_form_pattern(self, alpha_pattern: str) -> object:
        return self.get_graph_alpha_dict()[alpha_pattern]

    def get_duplicates(self, arr: List[object]) -> object:
        hashset = set()
        duplication = []
        for el in arr:
            if el not in hashset:
                hashset.add(el)
            else:
                duplication.append(el)
        return duplication

    def find_the_biggest_beta_node(self, exist_alpha_init_list: List[object]) -> List[object]:
        try:
            exist_alpha_inst_list = [ele[0] for ele in exist_alpha_init_list]
        except:
            exist_alpha_inst_list = [ele for ele in exist_alpha_init_list]
        exist_alpha_inst_Dict: Dict[str:object] = {}
        for node_obj in exist_alpha_inst_list:
            exist_alpha_inst_Dict[node_obj.get_pattern()] = node_obj

        # pprint(exist_alpha_inst_Dict)

        beta_node_list: List[object] = []
        for ele in exist_alpha_inst_list:
            beta_node_list += ele.get_edge_object_list()
        # print(self.get_duplicates(beta_node_list))
        duplicates: object = self.get_duplicates(beta_node_list)

        # no link
        if len(duplicates) == 0:
            return [None, {}]
        else:
            duplicates = duplicates[0]
        # print(duplicates)

        duplicates_left_node_pattern: str = duplicates.get_left_node().get_pattern()
        duplicates_right_node_pattern: str = duplicates.get_rigth_node().get_pattern()

        # print(duplicates_left_node_pattern)
        # print(duplicates_right_node_pattern)
        del exist_alpha_inst_Dict[duplicates_left_node_pattern]
        del exist_alpha_inst_Dict[duplicates_right_node_pattern]

        # pprint(exist_alpha_inst_Dict)

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
                return [highest, exist_alpha_inst_Dict]
            if flag == False:
                return [highest, exist_alpha_inst_Dict]
            flag = False

    def first_time_add_alpha_node(self, rule: str) -> None:
        if self.check_rule_form(rule) == False:
            raise Exception(f"This rule has some problem: {rule}")

        self._rule = rule
        pattern = self.split_rule_pattern_to_list(rule)

        for ele in pattern:
            alpha_node_inst: object = Alpha(ele)
            self.add_alpha_inst_to_temp_list(alpha_node_inst)
            self.add_alpha_inst_to_graph_dict(alpha_node_inst)

    def first_time_add_beta_node(self) -> None:
        rule_alpha_init_list: List[object] = self.get_alpha_inst_temp_list()

        try:
            rule_alpha_pattern_list: List[str] = [
                ele.get_pattern() for ele in rule_alpha_init_list]
        except:
            for ele in rule_alpha_init_list:
                print(ele.get_pattern())

        temp_beta_node_inst_list: List[object] = []

        for index in range(1, len(rule_alpha_init_list)):
            beta_pattern: str = "-".join(
                rule_alpha_pattern_list[: index + 1])

            if index == 1:
                left_node_init: object = rule_alpha_init_list[index-1]
                right_node_init: object = rule_alpha_init_list[index]
            else:
                left_node_init: object = temp_beta_node_inst_list[index-2]
                right_node_init: object = rule_alpha_init_list[index]

            beta_node_inst = Beta(
                beta_pattern, left_node_init, right_node_init)
            temp_beta_node_inst_list.append(beta_node_inst)
            self.add_beta_inst_to_graph_dict(beta_node_inst)
            self.notify_nodes_add_edge(
                beta_node_inst, left_node_init, right_node_init)

        self.empty_alpha_inst_temp_list()
        self._rule = ""

    def add_alpha_node(self, rule: str) -> None:
        if self.check_rule_form(rule) == False:
            raise Exception(f"This rule has some problem: {rule}")

        self._rule = rule
        alpha_pattern: List[str] = self.split_rule_pattern_to_list(rule)

        exist_alpha_nodes: List[str] = []
        new_alpha_nodes: List[str] = []
        exist_alpha_nodes, new_alpha_nodes = self.split_exist_alpha_nodes_and_new_alpha_nodes(
            alpha_pattern)
        self._alpha_pattern_temp_list = [exist_alpha_nodes, new_alpha_nodes]

        if new_alpha_nodes == []:
            return 0

        if exist_alpha_nodes == []:
            self.first_time_add_alpha_node(rule)
            return 0

        for ele in new_alpha_nodes:
            alpha_node_inst: object = Alpha(ele)
            self.add_alpha_inst_to_graph_dict(alpha_node_inst)

        for ele in alpha_pattern:
            alpha_node_init: object = self.get_alpha_node_init_form_pattern(
                ele)
            self.add_alpha_inst_to_temp_list(alpha_node_init)

    def add_NO_new_alpha_rule(self, rule: str) -> None:
        if self.check_rule_form(rule) == False:
            raise Exception(f"This rule has some problem: {rule}")
        alpha_pattern_list: List[str] = self.split_rule_pattern_to_list(rule)
        alpha_inst_list: List[object] = [
            self.get_alpha_node_init_form_pattern(ele)[0] for ele in alpha_pattern_list]

        all_edges: List[object] = []
        for ele in alpha_inst_list:
            all_edges += ele.get_edge_object_list()
            # print(sys._getframe().f_lineno, "ele.get_edge_object_list()",
            #       ele.get_edge_object_list())
        #print(sys._getframe().f_lineno, "all_edges", all_edges)
        betaNode = self.get_duplicates(all_edges)
        #print(sys._getframe().f_lineno, "betaNode", betaNode)
        if betaNode == []:
            temp_beta_node_list: List[object] = []
            for index in range(1, len(alpha_inst_list)):
                beta_pattern: str = "-".join(
                    alpha_pattern_list[: index + 1])
                if index == 1:
                    left_node_inst: object = alpha_inst_list[index-1]
                    right_node_inst: object = alpha_inst_list[index]
                else:
                    left_node_inst: object = temp_beta_node_list[index-2]
                    right_node_inst: object = alpha_inst_list[index]

                beta_node_inst: object = Beta(
                    beta_pattern, left_node_inst, right_node_inst)
                temp_beta_node_list.append(beta_node_inst)
                self.add_beta_inst_to_graph_dict(beta_node_inst)
                self.notify_nodes_add_edge(
                    beta_node_inst, left_node_inst, right_node_inst)

            self.empty_alpha_inst_temp_list()
            self._rule = ""
        else:
            highest, exist_alpha_inst_Dict = self.find_the_biggest_beta_node(
                alpha_inst_list)
            alpha_inst_list: List[object] = list(
                exist_alpha_inst_Dict.values())
            alpha_pattern_list: List[str] = list(exist_alpha_inst_Dict.keys())

            temp_beta_node_list: List[object] = [highest]

            for index in range(len(alpha_inst_list)):
                beta_pattern: str = temp_beta_node_list[index].get_pattern(
                ) + "-" + alpha_pattern_list[index]

                left_node_inst: object = temp_beta_node_list[index]
                right_node_inst: object = alpha_inst_list[index]

                beta_node_inst: object = Beta(
                    beta_pattern, left_node_inst, right_node_inst)
                temp_beta_node_list.append(beta_node_inst)
                self.add_beta_inst_to_graph_dict(beta_node_inst)
                self.notify_nodes_add_edge(
                    beta_node_inst, left_node_inst, right_node_inst)

            self.empty_alpha_inst_temp_list()
            self._rule = ""

    def add_beta_node(self) -> None:

        exist_alpha_nodes: List[str] = []
        new_alpha_nodes: List[str] = []
        exist_alpha_nodes, new_alpha_nodes = self._alpha_pattern_temp_list
        exist_alpha_node_init_list: List[object] = [
            self.get_alpha_node_init_form_pattern(ele) for ele in exist_alpha_nodes]
        new_alpha_node_init_list: List[object] = [
            self.get_alpha_node_init_form_pattern(ele) for ele in new_alpha_nodes]

        if new_alpha_node_init_list == []:
            self.add_NO_new_alpha_rule(self._rule)
            return 0
        if exist_alpha_nodes == []:
            self.first_time_add_beta_node()
            return 0

        biggest_beta_node_obj: object = None
        alpha_node_obj_list: List[object] = None
        biggest_beta_node_obj, alpha_node_obj_list = self.find_the_biggest_beta_node(
            exist_alpha_node_init_list)

        # if new_alpha_nodes
        alpha_node_obj_list = list(
            alpha_node_obj_list.keys()) + new_alpha_node_init_list
        alpha_node_obj_list = [ele[0] for ele in alpha_node_obj_list]

        temp_beta_node_inst_list: List[object] = [biggest_beta_node_obj
                                                  ]
        # have nothing link, need build all
        if temp_beta_node_inst_list == [None]:
            alpha_pattern_list: List[str] = self.split_rule_pattern_to_list(
                self._rule)

            alpha_inst_list: List[object] = []

            # add new alpha
            for ele in alpha_pattern_list:
                if ele in self.get_graph_alpha_dict():
                    alpha_inst_list.append(
                        self.get_alpha_node_init_form_pattern(ele))
                else:
                    alpha_node_inst: object = Alpha(ele)
                    alpha_inst_list.append(alpha_node_inst)
                    self.add_alpha_inst_to_graph_dict(alpha_node_inst)

            # add beta
            temp_beta_node_inst_list: List[object] = []
            for index in range(1, len(alpha_inst_list)):
                beta_pattern: str = "-".join(alpha_pattern_list[:index+1])
                if index == 1:
                    left_node_init: object = alpha_inst_list[index-1]
                    right_node_init: object = alpha_inst_list[index]
                else:
                    left_node_init: object = temp_beta_node_inst_list[index-2]
                    right_node_init: object = alpha_inst_list[index]
                print(isinstance(left_node_init, Alpha))
                print(right_node_init)
                beta_node_inst: object = Beta(
                    beta_pattern, left_node_init, right_node_init
                )
                print(left_node_init)
                print(right_node_init)
                temp_beta_node_inst_list.append(beta_node_inst)
                self.add_beta_inst_to_graph_dict(beta_node_inst)

                self.notify_nodes_add_edge(
                    beta_node_inst, left_node_init, right_node_init)

            self.empty_alpha_inst_temp_list()
            self._rule = ""
            return 0

        for index in range(len(alpha_node_obj_list)):
            beta_pattern = temp_beta_node_inst_list[index].get_pattern(
            ) + "-" + alpha_node_obj_list[index].get_pattern()

            left_node_init: object = temp_beta_node_inst_list[index]
            right_node_init: object = alpha_node_obj_list[index]

            beta_node_inst = Beta(
                beta_pattern, left_node_init, right_node_init)
            temp_beta_node_inst_list.append(beta_node_inst)
            self.add_beta_inst_to_graph_dict(beta_node_inst)
            self.notify_nodes_add_edge(
                beta_node_inst, left_node_init, right_node_init)
        self.empty_alpha_inst_temp_list()
        self._rule = ""
