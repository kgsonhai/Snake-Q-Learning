import pygame
import random
from collections import namedtuple
import Learner
import numpy as np
import time

pygame.init()

Point = namedtuple("Point", "x, y")

YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

BLOCK_SIZE = 20
DIS_WIDTH = 640
DIS_HEIGHT = 480
FRAMESPEED = 40


def GameLoop(learner):
    global dis
    dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
    pygame.display.set_caption("Snake AI Inference")
    clock = pygame.time.Clock()

    x1 = DIS_WIDTH // 2
    y1 = DIS_HEIGHT // 2
    snake_list = [Point(x1, y1)]

    x1_change = 0
    y1_change = 0
    length_of_snake = 1

    food = Point(
        round(random.randrange(0, DIS_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
        round(random.randrange(0, DIS_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
    )

    dead = False
    while not dead:
        pygame.event.get()  # Ensure the Pygame window updates

        action = learner.act(snake_list, food)
        if action == "left":
            x1_change = -BLOCK_SIZE
            y1_change = 0
        elif action == "right":
            x1_change = BLOCK_SIZE
            y1_change = 0
        elif action == "up":
            y1_change = -BLOCK_SIZE
            x1_change = 0
        elif action == "down":
            y1_change = BLOCK_SIZE
            x1_change = 0

        x1 += x1_change
        y1 += y1_change
        snake_head = Point(x1, y1)
        snake_list.append(snake_head)

        if (
            snake_head.x >= DIS_WIDTH
            or snake_head.x < 0
            or snake_head.y >= DIS_HEIGHT
            or snake_head.y < 0
            or snake_head in snake_list[:-1]
        ):
            dead = True

        if snake_head == food:
            food = Point(
                round(random.randrange(0, DIS_WIDTH - BLOCK_SIZE) / BLOCK_SIZE)
                * BLOCK_SIZE,
                round(random.randrange(0, DIS_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE)
                * BLOCK_SIZE,
            )
            length_of_snake += 1
        else:
            if len(snake_list) > length_of_snake:
                del snake_list[0]

        dis.fill(BLUE)
        DrawFood(food)
        DrawSnake(snake_list)
        DrawScore(length_of_snake - 1)
        pygame.display.update()

        clock.tick(FRAMESPEED)

    return length_of_snake - 1


def DrawFood(food):
    pygame.draw.rect(dis, GREEN, [food.x, food.y, BLOCK_SIZE, BLOCK_SIZE])


def DrawSnake(snake_list):
    for segment in snake_list:
        pygame.draw.rect(dis, BLACK, [segment.x, segment.y, BLOCK_SIZE, BLOCK_SIZE])
        pygame.draw.rect(dis, BLACK, [segment.x + 4, segment.y + 4, 12, 12])


def DrawScore(score):
    font = pygame.font.SysFont("comicsansms", 35)
    value = font.render(f"Score: {score}", True, YELLOW)
    dis.blit(value, [10, 10])


def KeepWindowOpen():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
    pygame.quit()


learner = Learner.Learner(DIS_WIDTH, DIS_HEIGHT, BLOCK_SIZE)
learner.LoadQvalues()

print("Running Snake AI Inference...")
score = GameLoop(learner)
print(f"Final Score: {score}")

time.sleep(2)  # Keeps the window visible for a moment before waiting for user input
KeepWindowOpen()
