import random
import math
import pygame

pygame.init()
font = pygame.font.SysFont("arial", 25)

# Window setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()
fps = 60


class Ball:
    def __init__(self):
        radius = 10

        self.speed = 5
        self.speed_increment = 0.2
        self.angle = random.choice([math.radians(random.randint(-45, 45)), math.radians(random.randint(135, 225))])
        self.rect = pygame.Rect(screen.get_width() // 2 - radius, screen.get_height() // 2 - radius, radius * 2, radius * 2)

        self.initial_speed = self.speed

    def move(self):
        self.rect.centerx = self.rect.centerx + math.cos(self.angle) * self.speed
        self.rect.centery = self.rect.centery + math.sin(self.angle) * self.speed
        self.check_window_collision()

    def check_window_collision(self):
        if self.rect.top <= 0:
            self.rect.top = 0  # prevent sticking
            self.angle = math.pi * 2 - self.angle
        elif self.rect.bottom >= screen.get_height():
            self.rect.bottom = screen.get_height()  # prevent sticking
            self.angle = math.pi * 2 - self.angle

    def check_player_collision(self, players):
        for player in players:
            ball_hits_paddle = ball.rect.colliderect(player)
            ball_moving_left = math.cos(ball.angle) < 0
            ball_moving_right = math.cos(ball.angle) > 0
            paddle_on_left = player.rect.centerx < ball.rect.centerx
            paddle_on_right = player.rect.centerx > ball.rect.centerx

            if ball_hits_paddle:
                if (paddle_on_left and ball_moving_left) or (paddle_on_right and ball_moving_right):
                    self.angle = math.pi - self.angle
                    self.speed += self.speed_increment


class Paddle:
    def __init__(self, player_id):
        width = 10
        height = 90
        dist = 30

        self.score = 0
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

        self.initial_pos = self.rect.topleft

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


def reset():
    for player in players:
        player.rect.topleft = player.initial_pos
    for ball in balls:
        ball.rect.center = [screen.get_width() // 2, screen.get_height() // 2]
        ball.speed = ball.initial_speed
    return False


game_over = False
while True:
    if game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_over = reset()
        over_msg = font.render("Game Over", True, "red")
        screen.blit(over_msg, [(screen.get_width() // 2) - (over_msg.get_width() // 2),
                               (screen.get_height() // 2) - (over_msg.get_height() // 2)])
        pygame.display.flip()
        continue

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

    for ball in balls:
        ball.move()
        ball.check_player_collision(players)

        # Scoring system
        if ball.rect.left <= 0:
            players[1].score += 1
            game_over = True
        elif ball.rect.right >= screen.get_width():
            players[0].score += 1
            game_over = True

    # Rendering
    screen.fill("black")
    for ball in balls:
        pygame.draw.circle(screen, "red", ball.rect.center, ball.rect.width // 2)
    for player in players:
        pygame.draw.rect(screen, player.color, player.rect)

    # Display scores
    score_text = font.render(f"{players[0].score}  -  {players[1].score}", True, "white")
    screen.blit(score_text, [(screen.get_width() // 2) - 20, 20])

    # Update Screen
    pygame.display.flip()
    clock.tick(fps)
