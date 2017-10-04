import pygame
import sys
import math
import random

import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS

import settings
from characters import Food, MainSnake, DangerousSnake, StickySnake


def distance_between_points(pos1, pos2):
    return math.sqrt(math.pow(pos1[0]-pos2[0], 2) + math.pow(pos1[1]-pos2[1], 2))


def snakes_touch(snake1, snake2):
    for snake1_part in snake1.body:
        for snake2_part in snake2.body:
            distance = distance_between_points(snake1_part.position, snake2_part.position)
            if distance < snake1_part.size + snake2_part.size:
                return True
    return False


def snake_touches_food(snake, food):
    snake_part = snake.body[0]
    distance = distance_between_points(snake_part.position, food.position)
    if distance < snake_part.size + food.size:
        return True
    return False


class Game(object):
    background_color = (22, 28, 34)

    game_started = False
    game_ended = False
    won = False
    round = 0

    foods = []
    dangerous_snakes = []
    sticky_snakes = []
    main_snake = None

    game_over_image = pygame.image.load('assets/game_over.png')
    title_image = pygame.image.load('assets/start.png')
    you_won_image = pygame.image.load('assets/you_won.png')

    def __init__(self, width, height):
        pygame.init()
        pygame.display.set_caption('Slither!')

        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((width, height))
        self.surface.fill(self.background_color)
        self.mouse_pos = pygame.mouse.get_pos()

    def reset_characters(self):
        self.foods = []

        self.dangerous_snakes = []
        self.sticky_snakes = []
        self.main_snake = None

    def clear_screen(self):
        self.surface.fill(self.background_color)
        pygame.display.flip()

    def start(self):
        self.game_started = True
        self.game_ended = False
        self.won = False

        # create all characters
        for x in range(settings.food_num):
            self.foods.append(Food(self.surface))

        self.main_snake = MainSnake(self.surface, self.mouse_pos)

    def game_over(self):
        self.game_started = False
        self.game_ended = True
        self.round = 0
        self.won = False

        self.reset_characters()
        self.clear_screen()

    def you_won(self):
        self.game_started = False
        self.game_ended = True
        self.round = 0
        self.won = True

        self.reset_characters()
        self.clear_screen()

    def restart(self):
        self.game_over()
        self.start()

    def run(self):
        while True:
            for event in GAME_EVENTS.get():
                self.check_for_quit(event)
                self.check_for_start(event)

            if self.game_started:
                self.round += 1
                self.surface.fill(self.background_color)

                self.mouse_pos = pygame.mouse.get_pos()

                self.create_extra_snakes()
                self.handle_movements()

                self.clock.tick(60)
                pygame.display.update()

            elif self.won:
                self.surface.blit(self.scale_image_to_screen(self.you_won_image), (0, 0))
                pygame.display.flip()

            elif self.game_ended:
                self.surface.blit(self.scale_image_to_screen(self.game_over_image), (0, 0))
                pygame.display.flip()

            else:
                self.surface.blit(self.scale_image_to_screen(self.title_image), (0, 0))
                pygame.display.flip()

    def handle_movements(self):
        for food in self.foods:
            if snake_touches_food(self.main_snake, food):
                self.foods.remove(food)
                self.main_snake.eat_food()

        for food in self.foods:
            food.glow()
            food.draw()

        self.main_snake.move(self.mouse_pos)

        if not self.foods:
            self.you_won()

        for snake in self.dangerous_snakes:
            snake.move()
            if snakes_touch(self.main_snake, snake):
                self.game_over()
            if snake.body[-1].position[0] > self.surface.get_width():
                self.dangerous_snakes.remove(snake)

        for sticky_snake in self.sticky_snakes:
            sticky_snake.move(self.mouse_pos)
            if snakes_touch(self.main_snake, sticky_snake):
                self.game_over()

    def create_extra_snakes(self):
        if self.round in settings.rounds_with_dangerous_snake:
            self.dangerous_snakes.append(
                DangerousSnake(
                    self.surface,
                    (0, random.randint(0, settings.window_height))))

        if self.round in settings.rounds_with_sticky_snake:
            self.sticky_snakes.append(
                StickySnake(
                    self.surface, (0, 0)))

    def scale_image_to_screen(self, image):
        return pygame.transform.scale(image, (self.surface.get_width(), self.surface.get_height()))

    def check_for_quit(self, event):
        if event.type == GAME_GLOBALS.QUIT:
            self.quit()

    def check_for_start(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not self.game_started:
                    self.start()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()


slither = Game(settings.window_width, settings.window_height)

slither.run()
