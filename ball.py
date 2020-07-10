"""Ball

This module an the implementation of the class Ball

Author: Alejandro Mujica (aledrums@gmail.com)
Date: 07/09/2020
"""
import pygame

from constants import VIRTUAL_HEIGHT, VIRTUAL_WIDTH

class Ball:
    """
    Game ball.
    """
    def __init__(self, x, y, size, color=(255, 255, 255)):
        """
        Init the ball.

        :param x: initial x coordinate.
        :param y: initial y coordinate.
        :param size: size for width and height.
        :param color: ball color.
        """
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.vx = 0
        self.vy = 0

    def get_collision_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)

    def collides(self, paddle):
        return self.get_collision_rect().colliderect(
            paddle.get_collision_rect()
        )

    def update(self, dt):
        """
        Update the ball for an elapsed time

        :param dt: The elapsed time.
        """
        self.x += self.vx*dt
        self.y += self.vy*dt        

    def render(self, surface):
        """
        Render the ball

        :param surface: The surface where the paddle is drawn on.
        """
        pygame.draw.rect(
            surface, self.color,
            pygame.Rect(int(self.x), int(self.y), self.size, self.size)
        )

    def reset(self):
        self.x = VIRTUAL_WIDTH//2 - 2
        self.y = VIRTUAL_HEIGHT//2 - 2
        self.vx = 0
        self.vy = 0

    def center(self):
        return (self.x + self.size//2, self.y + self.size//2)
