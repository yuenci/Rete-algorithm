"""
Author: Innis
Description: 
Date: 2022-03-31 23:58:23
LastEditTime: 2022-04-01 09:21:58
FilePath: \0328P-rete\animation.py
"""
"""
Author: Innis
Description: Visualization algorithm operation process
Date: 2022-03-31 23:58:23
LastEditTime: 2022-04-01 08:42:25
FilePath: \0328P-rete\animation.py
"""




import pygame
from typing import Dict, Tuple
class Window:
    def __init__(self, wigth: int, height: int) -> None:
        self.wigth: int = wigth
        self.height: int = height
        self.alpha_node_dict: Dict[str: Tuple[int, int]] = {}
        self.beta_node_dict: Dict[str: Tuple[int, int]] = {}
        self.circle_radius = 20
        self.font_size = 20

        self.window = None

    def conf(self) -> None:
        pygame.init()
        self.window = pygame.display.set_mode((self.wigth, self.height))
        pygame.display.set_caption("Rete Visualization")
        self.window.fill((15, 25, 49))
        pygame.display.flip()

    def add_alpha_node(self, pattern: str) -> None:
        if pattern in self.alpha_node_dict:
            print(f"[{pattern}] exist")
            return 0
        num = len(self.alpha_node_dict)
        x, y = 20 + num * self.circle_radius * 4, 40
        self.alpha_node_dict[pattern] = (x, y)
        pygame.draw.circle(self.window, (255, 255, 255),
                           (x, y), self.circle_radius, 3)

        x, y = 10 + num * self.circle_radius * 4, 26
        font = pygame.font.Font(
            "pygame\SourceCodePro-Regular.ttf", self.font_size)
        text = font.render(pattern, True, (255, 255, 255))
        self.window.blit(text, (x, y))

        pygame.display.update()

    def add_beta_node(
        self,
        beta_pattern: str,
        left_pattern: str,
        left_type: str,
        right_pattern: str,
        right_type: str,
    ) -> None:
        if left_type == "alpha":
            left_position = self.alpha_node_dict[left_pattern]
        elif left_type == "beta":
            left_position = self.beta_node_dict[left_pattern]
        if right_type == "alpha":
            right_position = self.alpha_node_dict[right_pattern]
        elif right_type == "beta":
            right_position = self.beta_node_dict[right_pattern]

        x = (left_position[0] + right_position[0]) / 2
        y = max(left_position[1], right_position[1]) + self.circle_radius * 4

        self.beta_node_dict[beta_pattern] = (x, y)
        pygame.draw.circle(self.window, (255, 255, 255),
                           (x, y), self.circle_radius, 3)

        font = pygame.font.Font(
            "pygame\SourceCodePro-Regular.ttf", self.font_size)
        text = font.render(beta_pattern, True, (255, 255, 255))
        self.window.blit(text, (x - 6, y - 14))

        left_line_start = (left_position[0], left_position[1])
        left_line_end = (x, y)
        pygame.draw.line(
            self.window, (255, 255, 255), left_line_start, left_line_end, 1
        )

        right_line_start = (right_position[0], right_position[1])
        right_line_end = (x, y)
        pygame.draw.line(
            self.window, (255, 255, 255), right_line_start, right_line_end, 1
        )

        pygame.display.update()
