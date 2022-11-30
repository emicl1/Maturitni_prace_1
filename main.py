"""
author = Alex Olivier Michaud
Hra Loď se vyhýbá meteoritům, loď se ovládá pomocí raspberry pico w

"""



import pygame
from sys import exit
from random import randint, uniform
from time import sleep
from multiprocessing import Process, Queue
from client import client, queue




def App():
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
    meteorit_x = randint(0, 800)
    meteorit_y = 0
    meteorit_x_2 = randint(0, 800)
    meteorit_y_2 = 0
    coin_x = randint(0, 800)
    coin_y = 0

    #rectangles
    ship_rect = ship.get_rect(midbottom=(ship_x, 800))
    meteorit_rect = meteorit.get_rect(midbottom=(meteorit_x, meteorit_y))
    meteorit_rect_2 = meteorit_2.get_rect(midbottom=(meteorit_x_2, meteorit_y_2))
    coin_rect = coin.get_rect(midbottom=(coin_x, coin_y))
    sky_surface_rect = sky_surface.get_rect(topleft=(0, 0))

    text_surface = font.render("Press Space to Start", True, (255, 255, 255))

    #speed
    meteorit_speed = 5
    meteorit_speed_2 = 5
    coin_speed = 5
    #speed in y
    meteorit_speed_y = 0
    meteorit_speed_y_2 = 0
    coin_speed_y = 0

    #rocket movement



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

        #print(queue.empty())
        if queue.empty() == False:
            data = queue.get().decode("utf-8")
            print(data)
            if ship_x > W:
                ship_x = W
            elif ship_x < 0:
                ship_x = 0
            elif data[0] >= ship_x:
                ship_x += 10
            elif data[0] <= ship_x:
                ship_x -= 10


        #moving objects, random sleep, random spawn, random speed
        if sky_surface_rect.colliderect(meteorit_rect) is False:
            meteorit_speed_y = uniform(-1*(800/meteorit_rect.left), 800/(800-meteorit_rect.left))
            meteorit_speed = randint(3, 10)
            meteorit_rect.top = 0

        if sky_surface_rect.colliderect(meteorit_rect_2) is False:
            meteorit_speed_y_2 = uniform(-1*(800/meteorit_rect_2.left), 800/(800-meteorit_rect_2.left ))
            meteorit_speed_2 = randint(3, 10)
            meteorit_rect_2.top = 0

        if sky_surface_rect.colliderect(coin_rect) is False:
            coin_speed_y = uniform(-1*(800/coin_rect.left), 800/(800-coin_rect.left))
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

        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    proc_2 = Process(target=App)
    proc_2.start()
    proc = Process(target=client, args=(queue,))
    proc.start()














