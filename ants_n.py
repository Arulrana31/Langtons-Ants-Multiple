import numpy as np
import random
import pygame
import time

pygame.init()

grid_size = 100

grid = np.zeros((grid_size, grid_size, 3), dtype=float)
# grid[ , , 0] represents the owner of the pheromones, grid[ , , 1] represents the probabilty , grid[ , , 2] represents the color of the grid


class ant:
    def __init__(self, x, y, dir, num):
        self.x = x
        self.y = y
        self.dir = dir
        self.num = num

    def change_dir(self):
        if grid[self.x, self.y, 2] == 0:
            self.dir = (self.dir - 1) % 4
        elif grid[self.x, self.y, 2] == 1:
            self.dir = (self.dir + 1) % 4

    def reverse_color(self):
        grid[self.x, self.y, 2] = (grid[self.x, self.y, 2] + 1) % 2

    def move(self):
        # 0 is down, 1 is right, 2 is up, 3 is left
        if self.dir == 0 and self.y > 0:
            self.y -= 1
            self.reverse_color()
        elif self.dir == 2 and self.y < grid_size - 1:
            self.y += 1
            self.reverse_color()
        elif self.dir == 1 and self.x < grid_size - 1:
            self.x += 1
            self.reverse_color()
        elif self.dir == 3 and self.x > 0:
            self.x -= 1
            self.reverse_color()


# Creating ants

n = int(input("Enter the number of ants: "))
ants = np.empty(n, dtype=ant)

for i in range(n):
    ant_test = ant(
        random.randint(0, grid_size - 1),
        random.randint(0, grid_size - 1),
        random.randint(0, 3),
        i,
    )
    ants[i] = ant_test

prob = 0.8
decay_time = 5


def update_pheromones():
    # pheromones decay
    for x in range(grid_size):
        for y in range(grid_size):
            grid[x, y, 1] = max(0, grid[x, y, 1] - prob / decay_time)


# Defining the grid for Pygame
grid_size = 100
cell_size = 10
width = grid_size * cell_size
height = grid_size * cell_size

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("ants")

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

running = True
while running:
    screen.fill(white)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    coord_prev = np.zeros((n, 2), dtype=int)
    for i in range(n):
        coord_prev[i, 0] = ants[i].x
        coord_prev[i, 1] = ants[i].y

    # ants moves
    for i in range(n):
        rand = random.random()
        if grid[ants[i].x, ants[i].y, 1] == 0:
            ants[i].change_dir()
            ants[i].move()
        elif grid[ants[i].x, ants[i].y, 0] == i:
            if rand < grid[ants[i].x, ants[i].y, 1]:
                ants[i].move()
            else:
                ants[i].change_dir()
                ants[i].move()

        else:
            if rand > grid[ants[i].x, ants[i].y, 1]:
                ants[i].move()
            else:
                ants[i].change_dir()
                ants[i].move()

    # Update pheromones and move ants
    update_pheromones()

    # update for tiles which have ants on them
    for i in range(n):
        grid[coord_prev[i, 0], coord_prev[i, 1], 0] = i
        grid[coord_prev[i, 0], coord_prev[i, 1], 1] = prob + prob / decay_time

    # displaying grid
    for x in range(grid_size):
        for y in range(grid_size):
            if grid[x, y, 1] > 0 and grid[x, y, 1] <= prob:
                color = (255 * grid[x, y, 1] / prob, 0, 0)
            elif grid[x, y, 2] == 0:
                color = white
            else:
                color = black
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size),
            )

    # displaying ants
    for i in range(n):
        pygame.draw.circle(
            screen,
            red,
            (
                ants[i].x * cell_size + cell_size // 2,
                ants[i].y * cell_size + cell_size // 2,
            ),
            cell_size // 2,
        )

    pygame.display.flip()

    # frame rate
    time.sleep(0.5)

# Quit Pygame
pygame.quit()
