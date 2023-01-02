"""Paddle

This module an the implementation of the class Paddle

Author: Alejandro Mujica (aledrums@gmail.com)
Date: 07/09/2020
"""
import pygame

from constants import VIRTUAL_HEIGHT


class Paddle:
    """
    Paddle to be controlled by a player
    """

    def __init__(self, x, y, width, height, color=(255, 255, 255)):
        """
        Init the paddle.

        :param x: initial x coordinate.
        :param y: initial y coordinate.
        :param width: paddle width.
        :param height: paddle height.
        :param color: paddle color.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.vy = 0

    def get_collision_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def update(self, dt):
        """
        Update the paddle for an elapsed time

        :param dt: The elapsed time.
        """
        next_y = self.y + self.vy*dt
        if self.vy < 0:
            self.y = max(0, next_y)
        else:
            self.y = min(VIRTUAL_HEIGHT - self.height, next_y)

    def render(self, surface):
        """
        Render the paddle

        :param surface: The surface where the paddle is drawn on.
        """
        pygame.draw.rect(
            surface, self.color,
            pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        )

    def center(self):
        return (self.x + self.width//2, self.y + self.height//2)
