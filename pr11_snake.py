import pygame, time, random

pygame.init()

WIDTH, HEIGHT = 600, 600
GRID_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = 20, 20

level, score = 1, 0
speed = 5
super_food_active = False

WHITE, RED, GREEN, YELLOW, BLUE, GRAY, BLACK, PURPLE = (255,255,255), (255,0,0), (0,255,0), (255,255,0), (0,0,255), (128,128,128), (0,0,0), (128,0,128)

screen = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption("Snake Game")

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

class Snake:
    def __init__(self):
        self.body = [Point(10,11), Point(10,12), Point(10,13)]
        self.dx, self.dy = 1, 0
    
    def move(self):
        for i in range(len(self.body)-1,0,-1):
            self.body[i].x, self.body[i].y = self.body[i-1].x, self.body[i-1].y
        self.body[0].x += self.dx
        self.body[0].y += self.dy
        if not (0 <= self.body[0].x < GRID_WIDTH and 0 <= self.body[0].y < GRID_HEIGHT):
            return False
        return True
    
    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.body[0].x*GRID_SIZE, self.body[0].y*GRID_SIZE, GRID_SIZE, GRID_SIZE))
        for seg in self.body[1:]:
            pygame.draw.rect(screen, YELLOW, (seg.x*GRID_SIZE, seg.y*GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    def check_collision(self, food, super_food):
        global score, super_food_active, level, speed
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            self.body.append(Point(head.x, head.y))
            score += food.weight
            food.change_pos()
            food.reset_timer()
        if super_food_active and head.x == super_food.pos.x and head.y == super_food.pos.y:
            self.body.append(Point(head.x, head.y))
            score += 2
            super_food.change_pos()
            super_food_active = False
        if score > level * 3:
            level += 1
            speed += 3

class Food:
    def __init__(self):
        self.weight = random.choice([1,2,3])
        self.pos = Point(random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
        self.timer = pygame.time.get_ticks()
    
    def reset_timer(self):
        self.timer = pygame.time.get_ticks()
    
    def change_pos(self):
        self.weight = random.choice([1,2,3])
        while True:
            new_pos = Point(random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
            if not any(new_pos.x == s.x and new_pos.y == s.y for s in snake.body):
                self.pos = new_pos
                break
    
    def draw(self):
        colors = {1: (205,127,50), 2: (192,192,192), 3: (255,215,0)}
        pygame.draw.rect(screen, colors[self.weight], (self.pos.x*GRID_SIZE, self.pos.y*GRID_SIZE, GRID_SIZE, GRID_SIZE))
        font = pygame.font.SysFont(None, 20)
        screen.blit(font.render(str(self.weight), True, BLACK), (self.pos.x*GRID_SIZE+10, self.pos.y*GRID_SIZE+8))

class SuperFood(Food):
    def __init__(self):
        self.pos = Point(random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
    def change_pos(self):
        while True:
            new_pos = Point(random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
            if not any(new_pos.x == s.x and new_pos.y == s.y for s in snake.body):
                self.pos = new_pos
                break
    def draw(self):
        pygame.draw.rect(screen, PURPLE, (self.pos.x*GRID_SIZE, self.pos.y*GRID_SIZE, GRID_SIZE, GRID_SIZE))
        font = pygame.font.SysFont(None, 20)
        screen.blit(font.render("+2", True, WHITE), (self.pos.x*GRID_SIZE+8, self.pos.y*GRID_SIZE+8))

clock = pygame.time.Clock()
snake = Snake()
food = Food()
super_food = SuperFood()

SUPER_FOOD_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SUPER_FOOD_EVENT, 3000)

font = pygame.font.SysFont("Verdana", 60)
game_over = font.render("Game Over", True, BLACK)

done = False
while not done:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dx, snake.dy = 1, 0
            elif event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx, snake.dy = -1, 0
            elif event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx, snake.dy = 0, 1
            elif event.key == pygame.K_UP and snake.dy != 1:
                snake.dx, snake.dy = 0, -1
        if event.type == SUPER_FOOD_EVENT:
            super_food_active = True
            super_food.change_pos()
    
    if current_time - food.timer > 5000:
        food.change_pos()
        food.reset_timer()
    
    screen.fill(GRAY)
    
    small_font = pygame.font.SysFont(None, 25)
    screen.blit(small_font.render(f"Score: {score}  Level: {level}", True, BLACK), (10, 10))
    screen.blit(small_font.render(f"Food weight: {food.weight}", True, BLACK), (10, 35))
    
    if not snake.move():
        done = True
        screen.fill(RED)
        screen.blit(game_over, (125, 225))
        pygame.display.update()
        time.sleep(2)
    
    snake.check_collision(food, super_food)
    if super_food_active:
        super_food.draw()
    snake.draw()
    food.draw()
    
    pygame.display.flip()
    clock.tick(speed)

pygame.quit()