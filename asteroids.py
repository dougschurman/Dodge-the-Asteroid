# Created by Doug Schurman
import pygame as pg
import random


pg.init()  # Loading Pygame
# Setting up display and images
display_width = 800
display_height = 600
game_display = pg.display.set_mode((display_width, display_height))
pg.display.set_caption('Dodge the Asteroid!')
stars = pg.image.load('starrynight.png')
icon = pg.image.load('asteroidicon.png')
pg.display.set_icon(icon)
menu_ship = pg.image.load('asteroidspaceship.png')

clock = pg.time.Clock()  # Keeping track of time


# Creating sprite classes to move ingame objects
class Spaceship(pg.sprite.Sprite):
    def __init__(self, startx, starty):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('asteroidspaceship.png')
        self.rect = self.image.get_rect()
        self.rect.x = startx
        self.rect.y = starty

    def move_left(self):
        if self.rect.x > 0:
            self.rect.x -= 5

    def move_right(self):
        if self.rect.x < 750:
            self.rect.x += 5

    def move_up(self):
        if self.rect.y > 0:
            self.rect.y -= 5

    def move_down(self):
        if self.rect.y < 550:
            self.rect.y += 5


class SmallAsteroid(pg.sprite.Sprite):
    def __init__(self, startx, starty):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('smallasteroid.png')
        self.rect = self.image.get_rect()
        self.rect.x = startx
        self.rect.y = starty

    def update(self, direct):
        if direct == 'left':
            self.rect.x += 3
        elif direct == 'top':
            self.rect.y += 3


class MediumAsteroid(pg.sprite.Sprite):
    def __init__(self, startx, starty):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('mediumasteroid.png')
        self.rect = self.image.get_rect()
        self.rect.x = startx
        self.rect.y = starty

    def update(self):
        self.rect.x -= 3


# Checking collisions between sprite groups and deleting group 1 if collided
def check_collide(group1, group2):
    collisions = pg.sprite.groupcollide(group1, group2, True, True)
    return collisions


# Displaying the score to the display
def score_count(score):
    font = pg.font.SysFont(None, 25)
    text = font.render('Score: ' + str(score), True, (255, 0, 0))
    game_display.blit(text, (0, 0))


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


# Dispays message from the object returend from text_objects
def message_display(text, x, y, color, size):
    largeText = pg.font.Font('freesansbold.ttf', size)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.center = (x, y)
    game_display.blit(TextSurf, TextRect)


# Creates a button with a chosen function
def button(msg, x, y, w, h, ic, ac, txtcolor, action=None):
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pg.draw.rect(game_display, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
            if action == pg.quit:
                quit()
    else:
        pg.draw.rect(game_display, ic, (x, y, w, h))

    smallText = pg.font.Font('freesansbold.ttf', 20)
    textSurf, textRect = text_objects(msg, smallText, txtcolor)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    game_display.blit(textSurf, textRect)


def game_loop():
    ship = Spaceship(375, 275)
    ships = pg.sprite.Group()
    ships.add(ship)
    # Creating lists and sprite groups for objects
    left_asteroids_list = []
    top_asteroids_list = []
    right_asteroids_list = []
    right_asteroids = pg.sprite.Group()
    top_asteroids = pg.sprite.Group()
    left_asteroids = pg.sprite.Group()
    # Keeping track of time to regulate output
    playing = True
    top_asteroid_time = 0
    left_asteroid_time = 0
    right_asteroid_time = 0
    score_time = 0
    score = 0
    while playing:
        dt = clock.tick(60)
        top_asteroid_time += dt
        left_asteroid_time += dt
        right_asteroid_time += dt
        score_time += dt
        for event in pg.event.get():  # Main way to check for clicking X
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        keys = pg.key.get_pressed()  # Dictionary to check keys pressed
        if keys[pg.K_a]:
            ship.move_left()
        if keys[pg.K_d]:
            ship.move_right()
        if keys[pg.K_w]:
            ship.move_up()
        if keys[pg.K_s]:
            ship.move_down()

        if score_time >= 1020:  # Keeping track of score almost every second
            score += 1
            score_time = 0
        # Regulating and creating randomly placed asteroids
        if top_asteroid_time > 1560:
            top_asteroids_list.append(SmallAsteroid(
                random.randint(0, 750), -50))
            top_asteroid_time = 0
        if left_asteroid_time > 1920:
            left_asteroids_list.append(
                SmallAsteroid(-50, random.randint(0, 550)))
            left_asteroid_time = 0
        if score > 30:
            if right_asteroid_time >= 2400:
                right_asteroids_list.append(
                    MediumAsteroid(900, random.randint(0, 500)))
                right_asteroid_time = 0

        game_display.blit(stars, (0, 0))
        ships.draw(game_display)
        left_asteroids.update('left')  # Moving asteroids if present
        top_asteroids.update('top')
        right_asteroids.update()
        # Drawing asteroids to display
        left_asteroids.draw(game_display)
        top_asteroids.draw(game_display)
        right_asteroids.draw(game_display)
        right_collides = check_collide(ships, right_asteroids)
        left_collides = check_collide(ships, left_asteroids)
        top_collides = check_collide(ships, top_asteroids)
        # Adding all asteroids to group
        right_asteroids.add(right_asteroids_list)
        left_asteroids.add(left_asteroids_list)
        top_asteroids.add(top_asteroids_list)
        score_count(score)
        if len(right_collides) > 0 or len(left_collides) > 0 or len(top_collides) > 0:
            playing = False  # Making sure if the ship collides the game stops
            end_screen(score)
        pg.display.flip()  # Refreshing display every loop
    return score


# Menu to display once the ship has crashed with buttons and score
def end_screen(score):
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        game_display.fill((0, 0, 0))
        message_display('You crashed!', (display_width / 2),
                        ((display_height / 2) - 100), (200, 0, 0), 115)
        message_display('Score: ' + str(score),
                        (display_width / 2), (display_height / 2), (200, 0, 0), 115)
        button('Play Again', 250, ((display_width / 2) + 100), 120, 50,
               (200, 0, 0), (255, 0, 0), (0, 0, 0), game_loop)
        button('Exit', 430, ((display_width / 2) + 100), 120,
               50, (200, 0, 0), (255, 0, 0), (0, 0, 0), pg.quit)
        pg.display.flip()


# Menu to start the game or exit
def start_menu():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        game_display.fill((0, 0, 0))
        message_display('Dodge the Asteroid!',
                        (display_width / 2), 100, (0, 255, 0), 60)
        message_display('Use WASD to move.',
                        (display_width / 2), 350, (0, 255, 0), 50)
        game_display.blit(menu_ship, (375, 200))
        button('Play', 250, ((display_width / 2) + 100), 120, 50,
               (0, 200, 0), (0, 255, 0), (0, 0, 0), game_loop)
        button('Exit', 430, ((display_width / 2) + 100), 120,
               50, (0, 200, 0), (0, 255, 0), (0, 0, 0), pg.quit)
        pg.display.flip()


start_menu()  # Starting the progression towards the game
pg.quit()  # Back up quit method and function to prevent Pygame from failing to quit
quit()
