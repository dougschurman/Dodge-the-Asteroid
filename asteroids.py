import pygame as pg
import random


pg.init()

display_width = 800
display_height = 600
game_display = pg.display.set_mode((display_width, display_height))
pg.display.set_caption('Dodge the Asteroid!')
stars = pg.image.load('starrynight.png')
icon = pg.image.load('asteroidicon.png')
pg.display.set_icon(icon)

clock = pg.time.Clock()


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


def game_loop():
    ship = Spaceship(300, 400)
    ships = pg.sprite.Group()
    ships.add(ship)
    asteroids = pg.sprite.Group()

    playing = True
    while playing:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            ship.move_left()
        if keys[pg.K_RIGHT]:
            ship.move_right()
        if keys[pg.K_UP]:
            ship.move_up()
        if keys[pg.K_DOWN]:
            ship.move_down()
        game_display.blit(stars, (0, 0))
        ships.draw(game_display)
        pg.display.flip()
        clock.tick(60)


game_loop()
pg.quit()
quit()
