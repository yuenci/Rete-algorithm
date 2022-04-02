'''
Author: Innis
Description: alpha node and beta node class
Date: 2022-04-02 09:24:50
LastEditTime: 2022-04-02 09:45:36
FilePath: \0328P-rete\0.5\node.py
'''
'''
Author: Innis
Description: alpha and beta nodes class
Date: 2022-04-01 14:04:59
LastEditTime: 2022-04-01 16:18:34
FilePath: \0328P-rete\0.4\node.py
'''




from typing import Union, List, Dict
from pprint import pprint
class Alpha:
    def __init__(self, pattern: str) -> None:
        self._pattern: str = pattern
        self._edges: Dict[object:int] = {}

    def get_pattern(self) -> str:
        return self._pattern

    def add_edge(self, beta_node_obj: object, weight: int) -> None:
        self._edges[beta_node_obj] = weight

    def get_edge_dict(self) -> Dict[object, int]:
        return self._edges

    def get_edge_object_list(self) -> List[object]:
        return list(self._edges.keys())


class Beta:
    def __init__(self, pattern: str, action: str, left_node: object, right_node: object, left_weight: int = 0, right_weight: int = 0) -> None:
        self._pattern: str = pattern
        self._action: str = action

        self._left_node: object = left_node
        self._right_node: object = right_node
        self._edges: Dict[object:int] = {}

        self.notify_nodes_add_edge(
            self, left_node, right_node, left_weight, right_weight)

    def get_pattern(self) -> str:
        return self._pattern

    def get_left_node(self) -> object:
        return self._left_node

    def get_rigth_node(self) -> object:
        return self._right_node

    def get_left_right_node_list(self) -> List[object]:
        return [self._left_node, self._right_node]

    def add_edge(self, beta_node_obj: object, weight=0) -> None:
        self._edges[beta_node_obj] = weight

    def get_edge_dict(self) -> Dict[object, int]:
        return self._edges

    def get_edge_object_list(self) -> List[object]:
        return list(self._edges.keys())

    def get_action(self) -> str:
        return self._action

    def notify_nodes_add_edge(self, original_beta_node: object, left_node_inst: object, right_node_inst: object, left_weight: int, right_weight: int) -> None:
        left_node_inst.add_edge(original_beta_node, left_weight)
        right_node_inst.add_edge(original_beta_node, right_weight)
