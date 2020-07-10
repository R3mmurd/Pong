"""
This module contains the implementation of an AI to play
the game.

Author: Alejandro Mujica (aledrums@gmail.com)
Date: 07/10/2020
"""

from constants import VIRTUAL_HEIGHT, PADDLE_SPEED

class PaddleAI:
    """
    AI than controls a paddle.
    """
    def __init__(self, game, paddle):
        self.ball = game.ball
        self.paddle = paddle

        if self.paddle == 1:
            self.me = game.paddle1
            self.another = game.paddle2
        else:
            self.me = game.paddle2
            self.another = game.paddle1

        self.paddle_dist = (
            game.paddle2.x - game.paddle1.x + game.paddle1.width
        )

    def update(self, dt):
        paddle_x, paddle_y = self.me.center()
        ball_x, ball_y = self.ball.center()
        ball_dist = abs(paddle_x - ball_x)
        prop = ball_dist/self.paddle_dist
    
        vision_height = prop*VIRTUAL_HEIGHT

        ball_comes = ((self.paddle == 1 and self.ball.vx < 0)
                        or (self.paddle == 2 and self.ball.vx > 0))

        if ball_comes and ball_y < paddle_y - vision_height:
            self.me.vy = -PADDLE_SPEED
        elif ball_comes and ball_y > paddle_y + vision_height:
            self.me.vy = PADDLE_SPEED
        else:
            self.me.vy = 0
        self.me.update(dt)
