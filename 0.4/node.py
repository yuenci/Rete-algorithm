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

    def add_edge(self, beta_node_obj: object, weight=0) -> None:
        self._edges[beta_node_obj] = weight

    def get_edge_dict(self) -> Dict[object, int]:
        return self._edges

    def get_edge_object_list(self) -> List[object]:
        return self._edges.keys()


class Beta:
    def __init__(self, pattern: str, left_node: object, right_node: object) -> None:
        self._pattern: str = pattern

        self._left_node: object = left_node
        self._right_node: object = right_node
        self._edges: Dict[object:int] = {}

        self._action: str = None

    def get_pattern(self) -> str:
        return self._pattern

    def get_left_node(self) -> object:
        return self._left_node

    def get_rigth_node(self) -> object:
        return self._right_node

    def add_edge(self, beta_node_obj: object, weight=0) -> None:
        self._edges[beta_node_obj] = weight

    def get_edge_dict(self) -> Dict[object, int]:
        return self._edges

    def get_edge_object_list(self) -> List[object]:
        return self._edges.keys()

    def set_action(self, action: str) -> None:
        self._action = action

    def get_action(self) -> str:
        return self._action
