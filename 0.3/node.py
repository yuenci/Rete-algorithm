'''
Author: Innis
Description: alpha node and beta node
Date: 2022-03-31 13:42:54
LastEditTime: 2022-04-01 10:38:50
FilePath: \0328P-rete\node.py
'''
from typing import Union, List, Dict
from pprint import pprint


class Alpha:
    def __init__(self, pattern: str) -> None:
        self.pattern: str = pattern
        self.edges: Dict[object:int] = {}
        self.activated_state: bool = False

    def add_edge(self, beta_node_obj: object, weight=0) -> None:
        self.edges[beta_node_obj] = weight

    def set_activated_state(self, state: bool) -> None:
        self.activated_state = state

    def get_activated_state(self) -> bool:
        return self.activated_state


class Beta:
    def __init__(self, pattern: str, left_node: object, right_node: object) -> None:
        self.pattern: str = pattern

        self.activated_state: bool = False

        self.left_node: object = left_node
        self.right_node: object = right_node
        self.edges: Dict[object:int] = {}

        self.action: str = None

    def get_pattern(self) -> str:
        return self.pattern

    def get_left_node(self) -> object:
        return self.left_node

    def get_rigth_node(self) -> object:
        return self.right_node

    def add_edge(self, beta_node_obj: object, weight=0) -> None:
        self.edges[beta_node_obj] = weight

    def set_activated_state(self, state: bool) -> None:
        self.activated_state = state

    def get_activated_state(self) -> bool:
        return self.activated_state

    def set_action(self, action: any) -> None:
        self.action = action
