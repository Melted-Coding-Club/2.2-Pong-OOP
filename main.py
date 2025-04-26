import pygame
import math

pygame.init()

# Window setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()
fps = 60


class Ball:
    def __init__(self):
        radius = 10

        self.speed = 5
        self.angle = 5
        self.rect = pygame.Rect(screen.get_width() // 2 - radius, screen.get_height() // 2 - radius, radius * 2, radius * 2)

    def move(self):
        self.rect.centerx = self.rect.centerx + math.cos(self.angle) * self.speed
        self.rect.centery = self.rect.centery + math.sin(self.angle) * self.speed


class Paddle:
    def __init__(self, player_id):
        width = 10
        height = 90
        dist = 30

        self.speed = 5
        if player_id == 0:
            self.rect = pygame.Rect(dist, screen.get_height() // 2 - height // 2, width, height)
            self.color = "blue"
            self.input_up = pygame.K_w
            self.input_down = pygame.K_s
        elif player_id == 1:
            self.rect = pygame.Rect(screen.get_width() - dist - width, screen.get_height() // 2 - height // 2, width, height)
            self.color = "green"
            self.input_up = pygame.K_UP
            self.input_down = pygame.K_DOWN

    def move(self, direction):
        if direction == "up":
            self.rect.y -= self.speed
        elif direction == "down":
            self.rect.y += self.speed
        self.check_window_collision()

    def check_window_collision(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height()

# Objects
balls = [Ball()]
players = [Paddle(0), Paddle(1)]

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Player controls
    pressed_keys = pygame.key.get_pressed()
    for player in players:
        if pressed_keys[player.input_up]:
            player.move("up")
        if pressed_keys[player.input_down]:
            player.move("down")

    # Ball movement
    for ball in balls:
        ball.move()

    # Rendering
    screen.fill("black")
    for ball in balls:
        pygame.draw.circle(screen, "red", ball.rect.center, ball.rect.width // 2)
    for player in players:
        pygame.draw.rect(screen, player.color, player.rect)

    # Update Screen
    pygame.display.flip()
    clock.tick(fps)
