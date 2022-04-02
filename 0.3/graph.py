"""
Author: Innis
Description: 
Date: 2022-03-31 13:43:34
LastEditTime: 2022-04-01 09:21:35
FilePath: \0328P-rete\graph.py
"""
"""
Author: Innis
Description: 
Date: 2022-03-31 13:43:34
LastEditTime: 2022-04-01 09:14:00
FilePath: \0328P-rete\graph.py
"""




from typing import Union, List, Dict
from pprint import pprint
from node import Alpha, Beta
class Graph:
    def __init__(self) -> None:
        self.graph_alpha_dict: Dict[str, object] = {}
        self.alpha_temp_list: List[object] = []

        self.graph_beta_dict: Dict[str, object] = {}

    def add_alpha_node_to_graph(self, rule: str) -> None:
        pattern: List[str] = [
            ele for ele in rule.split(" ") if ele != "if"][:-2]
        pattern = sorted(pattern)

        for ele in pattern:
            if ele in self.graph_alpha_dict:
                self.alpha_temp_list.append(alpha_object)
                continue
            alpha_object = self.create_and_get_alpha_node(ele)
            self.alpha_temp_list.append(alpha_object)
            self.graph_alpha_dict[alpha_object.pattern] = alpha_object

    def add_beta_node_to_graph(self) -> None:
        beta_nodes_List: List[object] = []
        alpha_node_list_with_exist_ones: List[object] = []
        for ele in self.alpha_temp_list:
            if ele.pattern in self.graph_alpha_dict:
                ele = self.graph_alpha_dict[ele]
                alpha_node_list_with_exist_ones.append(ele)
            else:
                alpha_node_list_with_exist_ones.append(ele)

        for index in range(1, len(alpha_node_list_with_exist_ones)):
            alpha_pattern_value: List[str] = [
                ele.pattern for ele in alpha_node_list_with_exist_ones]
            beta_pattern_value: List[str] = "-".join(
                alpha_pattern_value[: index + 1])

            if index == 1:
                if beta_pattern_value in self.graph_beta_dict:
                    beta_object = self.graph_beta_dict[beta_pattern_value]
                else:
                    beta_object: object = self.create_and_get_beta_node(
                        beta_pattern_value,
                        alpha_node_list_with_exist_ones[index - 1],
                        alpha_node_list_with_exist_ones[index],
                    )
                    alpha_node_list_with_exist_ones[index -
                                                    1].add_edge(beta_object)
                    alpha_node_list_with_exist_ones[index].add_edge(
                        beta_object)
            else:
                if beta_pattern_value in self.graph_beta_dict:
                    beta_object = self.graph_beta_dict[beta_pattern_value]

                beta_object: object = self.create_and_get_beta_node(
                    beta_pattern_value,
                    beta_nodes_List[index - 2],
                    alpha_node_list_with_exist_ones[index],
                )
                beta_nodes_List[index - 2].add_edge(beta_object)
                alpha_node_list_with_exist_ones[index].add_edge(beta_object)

            beta_nodes_List.append(beta_object)
            self.graph_beta_dict[beta_pattern_value] = beta_object
        self.alpha_temp_list = []

    def add_alpha_node(self, alpha_node: object) -> None:
        self.graph_alpha_dict[alpha_node.pattern] = alpha_node

    def add_beta_node(self, beta_node: object) -> None:
        self.graph_beta_dict[beta_node.pattern] = beta_node

    def create_and_get_alpha_node(self, pattern: str) -> None:
        return Alpha(pattern)

    def create_and_get_beta_node(
        self, pattern: str, left_node: object, right_node: object
    ) -> None:
        return Beta(pattern, left_node, right_node)

    def add_rule(self, rule: str) -> None:
        pattern: List[str] = [
            ele for ele in rule.split(" ") if ele != "if"][:-2]
        pattern = sorted(pattern)
        alpha_nodes_List: List[object] = []
        beta_nodes_List: List[object] = []

        # Create alpha nodes and add to graph dict
        for ele in pattern:
            alpha_object = self.create_and_get_alpha_node(ele)
            alpha_nodes_List.append(alpha_object)
            self.graph_alpha_dict[ele] = alpha_object

        # Create alpha nodes and add to graph dict
        for index in range(1, len(alpha_nodes_List)):
            beta_pattern_value = "-".join(pattern[: index + 1])
            if index == 1:
                beta_object = self.create_and_get_beta_node(
                    beta_pattern_value,
                    alpha_nodes_List[index - 1],
                    alpha_nodes_List[index],
                )
            else:
                beta_object = self.create_and_get_beta_node(
                    beta_pattern_value,
                    beta_nodes_List[index - 2],
                    alpha_nodes_List[index],
                )
            beta_nodes_List.append(beta_object)
            self.graph_beta_dict[beta_pattern_value] = beta_object

    def match(*patterns: str) -> Union[str, bool]:
        pass


# TODO this rule must has more than one pattern
