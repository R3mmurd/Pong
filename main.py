"""Main

Author: Alejandro Mujica (aledrums@gmail.com)
Date: 07/09/2020
"""

import sys
import random

import pygame

from paddle import Paddle
from ball import Ball
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, VIRTUAL_WIDTH, VIRTUAL_HEIGHT,
    PADDLE_SPEED, STATE_SERVE, STATE_START, STATE_PLAY, STATE_DONE, MAX_SCORE
)
from paddle_control import PaddleControl
from paddleAI import PaddleAI

pygame.init()


class PongGame:
    """
    Class to handle a Pong game.
    """

    game_fonts = {
            'small': pygame.font.Font('font.ttf', 8),
            'large': pygame.font.Font('font.ttf', 16),
            'score': pygame.font.Font('font.ttf', 32) 
        }

    game_sounds = {
            'paddle_hit': pygame.mixer.Sound('sounds/paddle_hit.wav'),
            'score': pygame.mixer.Sound('sounds/score.wav'),
            'wall_hit': pygame.mixer.Sound('sounds/wall_hit.wav')
        }

    key_pressed = {}

    def __init__(self, game_mode):
        # Setting the screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Pong')

        # Creating the virtual screen
        self.surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

        self.clock = pygame.time.Clock()

        self.ball = Ball(VIRTUAL_WIDTH//2 - 2, VIRTUAL_HEIGHT//2 - 2, 4)

        self.paddle1 = Paddle(10, 30, 5, 20)
        self.paddle2 = Paddle(VIRTUAL_WIDTH - 15, VIRTUAL_HEIGHT - 50, 5, 20)

        if game_mode == 0:
            self.player1 = PaddleAI(self, 1)
            self.player2 = PaddleAI(self, 2)
        elif game_mode == 1:
            self.player1 = PaddleControl(self, 1)
            self.player2 = PaddleAI(self, 2)
        elif game_mode == 2:
            self.player1 = PaddleAI(self, 1)
            self.player2 = PaddleControl(self, 2)
        else:
            self.player1 = PaddleControl(self, 1)
            self.player2 = PaddleControl(self, 2)

        self.player1_score = 0
        self.player2_score = 0

        self.serving_player = 0
        self.winning_player = 0

        self.game_state = STATE_START

    def render_text(self, text_str, font, x, y):
        text = self.game_fonts[font].render(text_str, True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (x, y)
        self.surface.blit(text, text_rect)

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                    else:
                        self.key_pressed[event.key] = True

            dt = self.clock.tick() / 1000
            self.update(dt)
            self.render()
            self.key_pressed = {}

    def update(self, dt):
        if self.game_state == STATE_START:
            if self.key_pressed.get(pygame.K_SPACE):
                self.serving_player = random.randint(1, 2)
                self.game_state = STATE_SERVE
        elif self.game_state == STATE_SERVE:
            if self.key_pressed.get(pygame.K_SPACE):
                self.ball.vy = random.randint(-50, 50)
                if self.serving_player == 1:
                    self.ball.vx = random.randint(140, 200)
                else:
                    self.ball.vx = -random.randint(140, 200)                
                self.game_state = STATE_PLAY
        elif self.game_state == STATE_PLAY:
            self.ball.update(dt)
            self.player1.update(dt)
            self.player2.update(dt)

            # Check ball collisions
            if self.ball.collides(self.paddle1):
                self.ball.x = self.paddle1.x + self.paddle1.width
                self.ball.vx = -self.ball.vx * 1.03
                self.game_sounds['paddle_hit'].play()

                if self.ball.vy < 0:
                    self.ball.vy = -random.randint(10, 150)
                else:
                    self.ball.vy = random.randint(10, 150)

            if self.ball.collides(self.paddle2):
                self.ball.x = self.paddle2.x - self.ball.size
                self.ball.vx = -self.ball.vx * 1.03
                self.game_sounds['paddle_hit'].play()

                if self.ball.vy < 0:
                    self.ball.vy = -random.randint(10, 150)
                else:
                    self.ball.vy = random.randint(10, 150)

            # Check collision with boundaries
            if self.ball.y < 0:
                self.ball.y = 0
                self.ball.vy *= -1
                self.game_sounds['wall_hit'].play()

            if self.ball.y + self.ball.size > VIRTUAL_HEIGHT:
                self.ball.y = VIRTUAL_HEIGHT - self.ball.size
                self.ball.vy *= -1
                self.game_sounds['wall_hit'].play()

            # Check if ball is out
            if self.ball.x < -self.ball.size:
                self.serving_player = 1
                self.player2_score += 1
                self.paddle1.vy = 0
                self.paddle2.vy = 0
                self.game_sounds['score'].play()

                if self.player2_score == MAX_SCORE:
                    self.game_state = STATE_DONE
                    self.winning_player = 2
                else:
                    self.ball.reset()
                    self.game_state = STATE_SERVE

            if self.ball.x > VIRTUAL_WIDTH:
                self.serving_player = 2
                self.player1_score += 1
                self.paddle1.vy = 0
                self.paddle2.vy = 0
                self.game_sounds['score'].play()

                if self.player1_score == MAX_SCORE:
                    self.game_state = STATE_DONE
                    self.winning_player = 1
                else:
                    self.ball.reset()
                    self.game_state = STATE_SERVE
        elif self.game_state == STATE_DONE:
            if self.key_pressed.get(pygame.K_SPACE):
                self.serving_player = random.randint(1, 2)
                self.winning_player = 0
                self.player1_score = 0
                self.player2_score = 0
                self.ball.reset()
                self.game_state = STATE_SERVE

    def render(self):
        self.surface.fill((40, 45, 52))

        if self.game_state == STATE_START:
            self.render_text('Welcome to Pong!', 'small',
                             VIRTUAL_WIDTH//2, 10
            )
            self.render_text('Press Space to begin!', 'small',
                             VIRTUAL_WIDTH//2, 20
            )
        elif self.game_state == STATE_SERVE:
            self.render_text(f"Player {self.serving_player}'s serve!",
                             'small', VIRTUAL_WIDTH//2, 10
            )
            self.render_text('Press Space to serve!', 'small',
                             VIRTUAL_WIDTH//2, 20
            )
        elif self.game_state == STATE_DONE:
            self.render_text(f"Player {self.winning_player} wins!", 'large',
                             VIRTUAL_WIDTH//2, 10
            )
            self.render_text('Press Space to restart!', 'small',
                             VIRTUAL_WIDTH//2, 30
            )

        # Display score
        self.render_text(
            str(self.player1_score), 'score',
            VIRTUAL_WIDTH//2-50, VIRTUAL_HEIGHT//3
        )
        self.render_text(
            str(self.player2_score), 'score',
            VIRTUAL_WIDTH//2+50, VIRTUAL_HEIGHT//3
        )

        self.ball.render(self.surface)
        self.paddle1.render(self.surface)
        self.paddle2.render(self.surface)

        self.screen.blit(
            pygame.transform.scale(self.surface, self.screen.get_size()),
            (0, 0)
        )
        pygame.display.update()


def main():
    game_mode = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    game = PongGame(game_mode)
    game.game_loop()
        

if __name__ == '__main__':
    main()