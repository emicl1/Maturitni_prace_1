"""
author = Alex Olivier Michaud
Hra Loď se vyhýbá meteoritům, loď se ovládá pomocí raspberry pico w

"""


import pygame
from sys import exit
from random import randint, uniform
from time import sleep
from multiprocessing import Process, Queue
from client import client

queue = Queue()

def App(queue):
    H = 800
    W = 1000

    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 30)


    #import images
    sky_surface = pygame.image.load("l.png")
    ship = pygame.image.load("ship.png").convert_alpha()
    meteorit = pygame.image.load("meteorit.png").convert_alpha()
    meteorit_2 = pygame.image.load("meteorit_2.png").convert_alpha()
    coin = pygame.image.load("coin.png").convert_alpha()

    #scale images
    ship = pygame.transform.scale(ship, (90, 90))
    meteorit = pygame.transform.scale(meteorit, (90, 90))
    meteorit_2 = pygame.transform.scale(meteorit_2, (90, 90))
    coin = pygame.transform.scale(coin, (90, 90))

    #coordinates
    ship_x = 450
    ship_y = 700
    meteorit_x = randint(0, 1000)
    meteorit_y = 0
    meteorit_x_2 = randint(0, 1000)
    meteorit_y_2 = 0
    coin_x = randint(0, 1000)
    coin_y = 0

    #rectangles
    ship_rect = ship.get_rect(midbottom=(ship_x, 800))
    meteorit_rect = meteorit.get_rect(midbottom=(meteorit_x, meteorit_y))
    meteorit_rect_2 = meteorit_2.get_rect(midbottom=(meteorit_x_2, meteorit_y_2))
    coin_rect = coin.get_rect(midbottom=(coin_x, coin_y))
    sky_surface_rect = sky_surface.get_rect(topleft=(0, 0))

    text_surface = font.render("Press Space to Start", True, (255, 255, 255))

    #speed
    ship_speed = 0
    meteorit_speed = 5
    meteorit_speed_2 = 5
    coin_speed = 5
    #speed in y
    meteorit_speed_y = 0
    meteorit_speed_y_2 = 0
    coin_speed_y = 0

    #rocket movement

    old_position = 0
    ship_state = "center"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        #spawning objects
        screen.blit(text_surface, (350, 200))
        screen.blit(sky_surface, (0, 0))
        screen.blit(ship, ship_rect)
        screen.blit(meteorit, meteorit_rect)
        screen.blit(meteorit_2, meteorit_rect_2)
        screen.blit(coin, coin_rect)


        if queue.empty() == False:
            print("not empty")
            data = queue.get()
            if ship_rect.right > W :
                ship_speed -= 5
                old_position = data[2]
            elif ship_rect.left < 0:
                ship_speed += 5
                old_position = data[2]
            elif data[2] >= old_position:
                ship_speed += 5
                old_position = data[2]
            elif data[2] <= old_position:
                ship_speed -= 5
                old_position = data[2]


        ship_rect.left += ship_speed





        #moving objects, random sleep, random spawn, random speed
        if sky_surface_rect.colliderect(meteorit_rect) is False:
            meteorit_speed_y = uniform(-1*(1000/meteorit_rect.left), 1000/(1000-meteorit_rect.left))
            meteorit_speed = randint(3, 10)
            meteorit_rect.top = 0

        if sky_surface_rect.colliderect(meteorit_rect_2) is False:
            meteorit_speed_y_2 = uniform(-1*(1000/meteorit_rect_2.left), 1000/(1000-meteorit_rect_2.left ))
            meteorit_speed_2 = randint(3, 10)
            meteorit_rect_2.top = 0

        if sky_surface_rect.colliderect(coin_rect) is False:
            coin_speed_y = uniform(-1*(1000/coin_rect.left), 1000/(1000-coin_rect.left))
            coin_speed = randint(3, 10)
            coin_rect.top = 0

        #moving objects
        meteorit_rect.top += meteorit_speed
        meteorit_rect_2.top += meteorit_speed_2
        coin_rect.top += coin_speed
        #moving objects in y
        meteorit_rect.left += meteorit_speed_y
        meteorit_rect_2.left += meteorit_speed_y_2
        coin_rect.left += coin_speed_y


        if meteorit_rect.colliderect(ship_rect):
            print("Collision")

        if meteorit_rect_2.colliderect(ship_rect):
            print("Collision")

        if coin_rect.colliderect(ship_rect):
            print("Collision")

        pygame.display.update()
        clock.tick(60)

def print_queue():
    while True:
        print(queue.get())



if __name__ == "__main__":
    queue = Queue()
    proc_2 = Process(target=App, args=(queue,))
    proc = Process(target=client, args=(queue,))
    proc.start()
    proc_2.start()
















