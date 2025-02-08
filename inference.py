import pygame
import random
import Learner  # Import the Learner class from the training file

pygame.init()

# Constants
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

BLOCK_SIZE = 10
DIS_WIDTH = 600
DIS_HEIGHT = 400

FRAMESPEED = 30  # Normal speed for visualization


def TestGame():
    global dis

    dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
    pygame.display.set_caption("Snake AI - Test Mode")
    clock = pygame.time.Clock()

    # Initialize starting position
    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2
    x1_change = 0
    y1_change = 0
    snake_list = [(x1, y1)]
    length_of_snake = 1

    # Generate the first food
    foodx = round(random.randrange(0, DIS_WIDTH - BLOCK_SIZE) / 10.0) * 10.0
    foody = round(random.randrange(0, DIS_HEIGHT - BLOCK_SIZE) / 10.0) * 10.0

    dead = False
    while not dead:
        # Handle quit event to prevent crashes
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # AI selects an action from pre-trained Q-values
        action = learner.act(snake_list, (foodx, foody))
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

        # Update snake position
        x1 += x1_change
        y1 += y1_change
        snake_head = (x1, y1)
        snake_list.append(snake_head)

        # Check if snake hits the screen boundary
        if x1 >= DIS_WIDTH or x1 < 0 or y1 >= DIS_HEIGHT or y1 < 0:
            print("AI died by hitting the screen boundary!")
            dead = True

        # Check if snake collides with itself
        if snake_head in snake_list[:-1]:
            print("AI died by colliding with itself!")
            dead = True

        # Check if snake eats the food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, DIS_WIDTH - BLOCK_SIZE) / 10.0) * 10.0
            foody = round(random.randrange(0, DIS_HEIGHT - BLOCK_SIZE) / 10.0) * 10.0
            length_of_snake += 1

        # Remove last cell if food is not eaten
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Render the game
        dis.fill(BLUE)
        DrawFood(foodx, foody)
        DrawSnake(snake_list)
        DrawScore(length_of_snake - 1)
        pygame.display.update()

        clock.tick(FRAMESPEED)  # Run at a normal speed for visualization

    print(f"AI achieved a score of: {length_of_snake - 1}")

    # Keep the window open after AI dies
    KeepWindowOpen()


def DrawFood(foodx, foody):
    pygame.draw.rect(dis, GREEN, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])


def DrawScore(score):
    font = pygame.font.SysFont("comicsansms", 35)
    value = font.render(f"Score: {score}", True, YELLOW)
    dis.blit(value, [0, 0])


def DrawSnake(snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, BLACK, [x[0], x[1], BLOCK_SIZE, BLOCK_SIZE])


def KeepWindowOpen():
    """Keep the pygame window open after AI dies"""
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
    pygame.quit()


# Initialize AI with pre-trained Q-values
learner = Learner.Learner(DIS_WIDTH, DIS_HEIGHT, BLOCK_SIZE)
learner.LoadQvalues()  # Load Q-values from the saved file
learner.epsilon = 0  # Disable random actions, only use optimal moves

# Run the test game
TestGame()
