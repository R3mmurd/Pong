"""
This module contains the implementation of a
class to control a pladdle.

Author: Alejandro Mujica (aledrums@gmail.com)
Date: 07/10/2020
"""
import pygame

from constants import PADDLE_SPEED


class PaddleControl:
    """
    Control for a paddle through the keyboard.
    """

    def __init__(self, game, paddle):
        if paddle == 1:
            self.paddle = game.paddle1
            self.key_up = pygame.K_w
            self.key_down = pygame.K_s
        else:
            self.paddle = game.paddle2
            self.key_up = pygame.K_UP
            self.key_down = pygame.K_DOWN

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[self.key_up]:
            self.paddle.vy = -PADDLE_SPEED
        elif keys[self.key_down]:
            self.paddle.vy = PADDLE_SPEED
        else:
            self.paddle.vy = 0
        self.paddle.update(dt)
