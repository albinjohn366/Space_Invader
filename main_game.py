import pygame
import random
import math

pygame.init()


# Function to load images
def load_image(path):
    return pygame.image.load(path)


# Defining a class for GUI
class GUI:

    # Initializing all the basic requirements
    def __init__(self, width, length):
        self.screen = pygame.display.set_mode((width, length))
        pygame.display.set_caption('Space Invaders')
        icon = load_image('space-invaders.png')
        pygame.display.set_icon(icon)
        pygame.display.update()

        self.player_image = load_image('player.png')
        self.player_image_transformed = pygame.transform.scale(
            self.player_image, (140, 80))
        self.enemy_image = pygame.transform.scale(load_image('enemy.png'),
                                                  (60, 60))
        self.background = pygame.transform.scale(load_image('background.png'),
                                                 (900, 500))
        self.background_text = pygame.transform.scale(load_image(
            'space_invader_text.png'), (500, 200))
        self.bullet_image = pygame.transform.scale(load_image('bullet.png'),
                                                   (20, 30))

        self.player_x = 60
        self.player_y = 420

        # Creating dictionaries for multiple bullets
        self.bullet_x = dict()
        self.bullet_y = dict()
        self.bullet_y[1] = 420
        self.bullet_x[1] = -20

        # Score sheet
        self.score = 0
        self.score_font = pygame.font.Font('Almond Caramel.ttf', 32)
        self.g_o = False

        # Creating dictionary for multiple enemies
        self.enemy_x = dict()
        self.enemy_y = dict()
        self.enemy_x_change = dict()
        for i in range(1, 6):
            self.enemy_x[i] = random.randint(0, width - 70)
            self.enemy_y[i] = random.randint(0, 200)
            self.enemy_x_change[i] = 3

    # Show score
    def show_score(self):
        score = self.score_font.render('Score: {}'.format(str(self.score)),
                                       True, (255, 255, 255))
        self.screen.blit(score, (10, 10))
        if self.score % 10 == 0 and self.score != 0:
            for key in self.enemy_x_change.keys():
                self.enemy_x_change[key] += 0.1

    # Separate function for player
    def player(self, x, y):
        self.screen.blit(self.player_image_transformed, (x, y))

    # Separate function for enemy
    def enemy(self, x, y):
        self.screen.blit(self.enemy_image, (x, y))

    # Bullet movement
    def bullet_movement(self):
        for key in self.bullet_y.keys():
            self.screen.blit(self.bullet_image, (self.bullet_x[key],
                                                 self.bullet_y[key]))
            self.bullet_y[key] -= 4

    # Enemy movements towards player
    def enemy_movement(self):
        for key in self.enemy_y.keys():
            self.enemy(self.enemy_x[key], self.enemy_y[key])
            if self.enemy_x[key] >= width - 60 or self.enemy_x[key] <= 0:
                self.enemy_y[key] += 40
                self.enemy_x_change[key] *= -1
            self.enemy_x[key] += self.enemy_x_change[key]

            distance = math.sqrt((self.enemy_y[key] - self.player_y) ** 2 + (
                    self.enemy_x[key] - self.player_x) ** 2)
            if distance < 27:
                self.game_over()

    # Game Over
    def game_over(self):
        self.g_o = True
        self.screen.fill((0, 0, 0))
        game_over_image = pygame.transform.scale(load_image(
            'game_over.png'), (200, 200))
        self.screen.blit(game_over_image, (200, 200))

    # Checking for collision
    def collision_check(self):
        for enemy_key in self.enemy_y.keys():
            for bullet_key in self.bullet_y.keys():
                distance = math.sqrt((self.enemy_y[enemy_key] - self.bullet_y[
                    bullet_key]) ** 2 + (self.enemy_x[enemy_key] -
                                         self.bullet_x[bullet_key]) ** 2)
                if distance < 27:
                    self.score += 1
                    self.enemy_y[enemy_key] = random.randint(0, 200)
                    self.enemy_x[enemy_key] = random.randint(0, width - 70)


if __name__ == '__main__':
    # Height and width of the window
    width = 600
    height = 500
    gui = GUI(width, height)

    # Bgm for the game
    pygame.mixer.music.load('kickstarter.wav')
    pygame.mixer.music.play(-1)
    bullet_sound = pygame.mixer.Sound('bullet_sound.wav')

    # Counts for enemies and bullets
    bullet_count = 1
    enemy_count = 1

    running = True
    x_change = 0
    while running:
        if not gui.g_o:
            gui.screen.fill((0, 0, 0))
            gui.screen.blit(gui.background, (0, 0))
            gui.screen.blit(gui.background_text, (50, 120))

        # Doing operations on each event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -4
                elif event.key == pygame.K_RIGHT:
                    x_change = +4
                elif event.key == pygame.K_SPACE:
                    gui.bullet_x[bullet_count] = gui.player_x + 61
                    gui.bullet_y[bullet_count] = 420
                    bullet_count += 1
                    bullet_sound.play()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        new_value = gui.player_x + x_change
        if -70 <= new_value <= width - 70:
            gui.player_x = new_value
        gui.player(gui.player_x, gui.player_y)
        if not gui.g_o:
            gui.enemy_movement()
            gui.bullet_movement()
            gui.collision_check()
            gui.show_score()
            pygame.display.update()
