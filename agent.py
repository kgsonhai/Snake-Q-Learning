import pygame
import random
from collections import namedtuple
import Learner
from collections import deque
import numpy as np

pygame.init()

Point = namedtuple("Point", "x, y")

YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

BLOCK_SIZE = 20
DIS_WIDTH = 640
DIS_HEIGHT = 480
QVALUES_N = 100
FRAMESPEED = 50


def GameLoop(learner):
    global dis

    dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
    pygame.display.set_caption("Snake AI Training")
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
    reason = None
    while not dead:
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
        ):
            reason = "Screen"
            dead = True

        if snake_head in snake_list[:-1]:
            reason = "Tail"
            dead = True

        if snake_head == food:
            food = Point(
                round(random.randrange(0, DIS_WIDTH - BLOCK_SIZE) / BLOCK_SIZE)
                * BLOCK_SIZE,
                round(random.randrange(0, DIS_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE)
                * BLOCK_SIZE,
            )
            length_of_snake += 1

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        dis.fill(BLUE)
        DrawFood(food)
        DrawSnake(snake_list)
        DrawScore(length_of_snake - 1)
        pygame.display.update()

        learner.UpdateQValues(reason)

        clock.tick(FRAMESPEED)

    return length_of_snake - 1, reason


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


game_count = 1
scores = []
rolling_window = deque(maxlen=100)
total_score = 0


learner = Learner.Learner(DIS_WIDTH, DIS_HEIGHT, BLOCK_SIZE)
record = 0

with open("output.txt", "a") as file:
    for game_count in range(1, 2001):
        learner.Reset()

        if game_count > 200:
            learner.epsilon = 0
        else:
            learner.epsilon = 0.1

        score, reason = GameLoop(learner)
        total_score += score
        scores.append(score)

        rolling_window.append(score)
        rolling_mean_score = np.mean(rolling_window)

        if score > record:
            record = score

        file.write(f"{game_count} {score} {rolling_mean_score}\n")

        print(
            f"Game: {game_count}; Score: {score}; Record: {record}; Mean: {rolling_mean_score}"
        )

        if game_count % QVALUES_N == 0:
            print("Saving Q-values...")
            learner.SaveQvalues()
