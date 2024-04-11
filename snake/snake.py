import pygame
from color_palette import *
import random
import time

pygame.init()

WIDTH = 600
HEIGHT = 600
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
CELL = 30
FPS = 5

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, colorBLACK)

level = 1
score = 0
timer_event = pygame.USEREVENT + 1 

def draw_grid():
    for i in range(HEIGHT // 2):
        for j in range(WIDTH // 2):
            pygame.draw.rect(DISPLAYSURF, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)

def draw_grid_chess():
    colors = [colorWHITE, colorGRAY]

    for i in range(HEIGHT // 2):
        for j in range(WIDTH // 2):
            pygame.draw.rect(DISPLAYSURF, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0
        self.is_alive = True

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(DISPLAYSURF, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(DISPLAYSURF, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))
        food.draw()

    def check_collision(self, food):
        global score, level, FPS
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            print("Got food!")
            if food.color == colorGREEN: 
                score += 1
            elif food.color == colorRED: 
                score += 3
            elif food.color == colorBLACK:
                score -= 1
            elif food.color == colorYELLOW:
                score += 2
            self.body.append(Point(head.x, head.y))
            food.random_food()
            food.redraw()
        if score >= level * 5:
            level += 1
            FPS = FPS + 0.5


    def check_wall(self):
        head = self.body[0]
        if head.x == 20 or head.y == 20 or head.x == -1 or head.y == -1:
            print("Game over")
            self.is_alive = False

    def check_yourself(self):
        for i in range(1, len(self.body) - 1):
            if self.body[0].x == self.body[i].x and self.body[0].y == self.body[i].y:
                print("Game over")
                self.is_alive = False

class Food:
    def __init__(self):
        self.pos = Point(random.randint(0, 19), random.randint(0, 19))
        self.color = colorGREEN
        self.timer_started = False

    def apple(self):
        self.color = colorGREEN


    def rotten_apple(self):
        self.color = colorBLACK

        if not self.timer_started:
            pygame.time.set_timer(timer_event, 5000)
            self.timer_started = True

    def tomato(self):
        self.color = colorRED


    def lemon(self):
        self.color = colorYELLOW
 



    food_list = [apple, rotten_apple, tomato, lemon]

    def random_food(self):
        random_func = random.choice(self.food_list)
        random_func(self)

    def draw(self):
        pygame.draw.rect(DISPLAYSURF, self.color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def redraw(self):
        new_pos = Point(random.randint(0, 19), random.randint(0, 19))
        for i in range(0, len(snake.body)):
            if snake.body[i].x == new_pos.x and snake.body[i].y == new_pos.y:
                while snake.body[i].x == new_pos.x and snake.body[i].y == new_pos.y:
                    new_pos = Point(random.randint(0, 19), random.randint(0, 19))
                    self.pos = new_pos
                    print("coincidence")
            else:
                self.pos = new_pos


current_color = [0, 255, 0]

clock = pygame.time.Clock()
food = Food()
snake = Snake()

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT:
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN:
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP:
                snake.dx = 0
                snake.dy = -1
        if event.type == timer_event and food.color == colorBLACK:
            food.color = colorGREEN
            food.pos = Point(random.randint(0, 19), random.randint(0, 19))
            food.timer_started = False

    draw_grid_chess()
    snake.move()
    snake.draw()
    snake.check_collision(food)
    snake.check_wall()
    snake.check_yourself()

    if snake.is_alive == False:
        DISPLAYSURF.fill(colorRED)
        DISPLAYSURF.blit(game_over, (100, 150))
        DISPLAYSURF.blit(level_counter, (125, 250))
        DISPLAYSURF.blit(food_counter, (125, 300))
        pygame.display.update()
        time.sleep(3)
        done = True

    level_counter = font_small.render("level: " + str(level), True, colorBLACK)
    food_counter = font_small.render("score: " + str(score), True, colorBLACK)
    DISPLAYSURF.blit(level_counter, (20, 10))
    DISPLAYSURF.blit(food_counter, (WIDTH - 100, 10))

    pygame.display.flip()
    clock.tick(FPS)
