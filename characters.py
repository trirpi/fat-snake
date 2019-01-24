import random
import pygame
import settings
import math

from collections import deque
from pygame import gfxdraw


class Food(object):
    size = 5
    glowing = False
    round = True

    def __init__(self, surface):
        self.surface = surface
        self.color = _get_random_color()
        self.position = (random.randint(0, settings.window_width),
                         random.randint(0, settings.window_height))
        self.draw()

    def draw(self):
        gfxdraw.aacircle(
            self.surface,
            self.position[0],
            self.position[1],
            self.size,
            self.color)
        gfxdraw.filled_circle(
            self.surface,
            self.position[0],
            self.position[1],
            self.size,
            self.color)

    def glow(self):
        self.round += 1
        if (self.round % 5) == 0:
            if random.randint(0, 10) == 2:
                self.size += 1
                self.glowing += 1
            elif random.randint(0, 5) == 2:
                if self.glowing > 0:
                    self.size -= 1
                    self.glowing -= 1
            elif self.glowing > 5:
                self.size -= 1
                self.glowing -= 1


class _SnakeBodyPart(object):
    def __init__(self, surface, color, position, size):
        self.surface = surface
        self.color = color
        self.position = position
        self.size = size

        pygame.draw.circle(surface, color, self.position, size)

    def move(self, next_pos):
        self.position = next_pos
        self.draw()

    def draw(self):
        pygame.draw.circle(self.surface, self.color, self.position, self.size)


class MainSnake(object):

    def __init__(self, surface, position):
        self.body = deque([])  # body made out of circles
        self.speed = 5
        self.size = 30
        self.color = (0, 0, 255)
        self.length = 5

        self.food_to_grow = 5
        self.food_eated = 0
        self.surface = surface
        for x in range(self.length):
            self.body.append(_SnakeBodyPart(surface, self.color, position, self.size))

    def eat_food(self):
        self.food_eated += 1
        if self.food_eated >= self.food_to_grow:
            self.food_eated = 0
            self.length += 1

            self.body.append(
                _SnakeBodyPart(
                    self.surface,
                    self.color,
                    self.body[-1].position,
                    self.size))

    def move(self, mouse_pos):
        snake_head_pos = self.body[0].position

        width_difference = mouse_pos[0] - snake_head_pos[0]
        height_difference = mouse_pos[1] - snake_head_pos[1]

        angle = math.atan2(height_difference, width_difference)

        next_pos_x = snake_head_pos[0] + math.cos(angle) * self.speed
        next_pos_y = snake_head_pos[1] + math.sin(angle) * self.speed

        self.body.rotate(1)
        self.body[0].move((int(next_pos_x), int(next_pos_y)))
        self.draw()

    def draw(self):
        for body_part in self.body:
            body_part.draw()


class DangerousSnake:

    def __init__(self, surface, position):
        self.body = deque([])  # body made out of circles
        self.speed = 5
        self.size = 20
        self.color = (255, 0, 0)
        self.length = 50
        self.surface = surface
        for x in range(self.length):
            self.body.append(_SnakeBodyPart(surface, self.color, position, self.size))

    def draw(self):
        for body_part in self.body:
            body_part.draw()

    def move(self):
        next_pos = (self.body[0].position[0] + self.speed, self.body[0].position[1])
        self.body.rotate(1)
        self.body[0].move(next_pos)
        self.draw()


class StickySnake(object):

    def __init__(self, surface, position):
        self.body = deque([])  # body made out of circles
        self.speed = 2
        self.size = 15
        self.color = (102, 204, 26)
        self.length = 20

        self.surface = surface
        for x in range(self.length):
            self.body.append(_SnakeBodyPart(surface, self.color, position, self.size))

    def move(self, main_snake_head_pos):
        snake_head_pos = self.body[0].position

        width_difference = main_snake_head_pos[0] - snake_head_pos[0]
        height_difference = main_snake_head_pos[1] - snake_head_pos[1]

        angle = math.atan2(height_difference, width_difference)

        next_pos_x = snake_head_pos[0] + math.cos(angle) * self.speed
        next_pos_y = snake_head_pos[1] + math.sin(angle) * self.speed

        self.body.rotate(1)
        self.body[0].move((int(next_pos_x), int(next_pos_y)))
        self.draw()

    def draw(self):
        for body_part in self.body:
            body_part.draw()


def _get_random_color():
    return (random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255))


class DangerousWarning(object):

    def __init__(self, surface, position):
        self.surface = surface
        self.color = pygame.Color(255,0,0)
        self.width = 10
        self.position = (self.width, position[1])
        self.disappear = 50

    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.position[0], self.position[1], self.width, 20))
        pygame.draw.rect(self.surface, self.color, (self.position[0], self.position[1]+25, self.width,5))

        self.disappear -= 1
        if self.disappear == 0:
            return True
        return False

class StickyWarning(object):

    def __init__(self, surface, position):
        self.surface = surface
        self.color = pygame.Color(255,0,0)
        self.width = 10
        self.position = (self.width, position[1])
        self.disappear = 50

    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.position[0], self.position[1], self.width, 20))
        pygame.draw.rect(self.surface, self.color, (self.position[0], self.position[1]+25, self.width,5))

        self.disappear -= 1
        if self.disappear == 0:
            return True
        return False
